<template>
    <!-- Sidebar -->
    <aside class="expert-sidebar">
        <!-- 타겟팅 목적 선택 -->
        <div class="expert-sidebar-header">
            <p class="mb-0 text-muted" v-if="!selectedTargetGroupArea">
                타겟팅 목적을 선택하세요.
            </p>
            <h4 class="mb-0 text-truncate" v-else>
                {{ selectedTargetGroupArea.targetAreaGroupName }}
            </h4>
            <b-button
                variant="ghost-light"
                class="btn-icon rounded-circle"
                title="타겟팅조건 변경"
                @click="showTargetGroupModal()"
            >
                <i class="ti ti-list-search"></i>
            </b-button>
        </div>

        <!-- 주제영역 -->
        <div class="expert-subject">
            <label for="basiInput" class="form-label">주제영역</label>
            <b-form-select
                v-model="selectedTargetAreaId"
                @change="targetAreaSelected(selectedTargetAreaId)"
            >
                <b-form-select-option
                    v-for="item in targetAreaList"
                    :value="item.targetAreaId"
                    v-bind:key="item.targetAreaId"
                    >{{ item.targetAreaName }}
                </b-form-select-option>
            </b-form-select>
        </div>

        <!-- 관점 검색 -->
        <div class="expert-viewpoint-wrap">
            <div class="viewpoint-filter">
                <!-- Viewpoint Search-->
                <form class="expert-viewpoint-search">
                    <div class="position-relative">
                        <input
                            type="text"
                            class="form-control"
                            v-model="treeSearchText"
                            placeholder="검색어 입력"
                            autocomplete="off"
                            @keydown.enter.prevent="onTreeSearch"
                        />
                        <span
                            class="ti ti-search search-widget-icon"
                            @click="onTreeSearch"
                        ></span>
                        <span
                            class="ti ti-circle-x-filled search-widget-icon search-widget-icon-close d-none"
                            id="search-close-options"
                        ></span>
                    </div>
                    <div class="hstack justify-content-between">
                        <div class="hstack gap-1">
                            <b-button
                                variant="light"
                                size="xs"
                                class="btn-icon"
                                @click="treeExpandAll"
                            >
                                <i class="ti ti-plus"></i>
                            </b-button>
                            <b-button
                                variant="light"
                                size="xs"
                                class="btn-icon"
                                @click="treeCollapseAll"
                            >
                                <i class="ti ti-minus"></i>
                            </b-button>
                        </div>
                        <b-FormGroup class="form-check-primary hstack gap-3">
                            <b-FormCheckbox v-model="checkedField">
                                관점 값 확장 검색
                            </b-FormCheckbox>
                            <b-FormCheckbox
                                v-model="checkedFieldFlag"
                                :disabled="!checkedField"
                            >
                                완전 일치
                            </b-FormCheckbox>
                        </b-FormGroup>
                    </div>
                </form>
            </div>

            <!-- expert-viewpoint-list -->
            <Simplebar class="expert-viewpoint-list">
                <!-- metaTableList 값이 있고, 길이가 0보다 크면 AntTree 출력 -->
                <AntTree
                    v-if="metaTableList && metaTableList.length > 0"
                    :tree-data="displayList"
                    :search-text="appliedSearch"
                    :checked-field="checkedField"
                    :api-keys="apiKeys"
                    :expanded-keys="expandedKeys"
                    @update:expanded-keys="(keys) => (expandedKeys = keys)"
                    @node-drag-start="onDragStart"
                />
                <!-- Empty Message -->
                <EmptyMessage v-else>조회된 관점정보가 없습니다.</EmptyMessage>
            </Simplebar>
        </div>
        <ExpertPerspectiveCollectionModal />
    </aside>
    <!-- Contents -->
    <Simplebar class="expert-content">
        <b-row class="row-cols-1">
            <b-col>
                <!-- Card: 타겟팅 조건 -->
                <b-card
                    class="tc-panel"
                    header-class="d-flex align-items-end gap-2"
                    footer-class="py-3"
                >
                    <!--Header-->
                    <template #header>
                        <h4 class="card-title mb-0">타겟팅 조건</h4>
                        <p class="card-subtitle text-muted">
                            <strong class="text-info">{{
                                flattenedList.length
                            }}</strong
                            >개의 관점이 추가되었습니다.
                        </p>
                        <b-button
                            variant="light-2"
                            class="ms-auto"
                            @click="resetTargetingList()"
                        >
                            <i class="ti ti-refresh"></i>조건 초기화
                        </b-button>
                    </template>
                    <!--Body-->

                    <!-- 타겟팅 조건 트리메뉴 -->
                    <div
                        class="tc-tree-wrapper"
                        v-show="flattenedList.length > 0"
                    >
                        <ul class="tc-tree-root">
                            <li
                                class="tc-tree-node"
                                v-for="(node, idx) in flattenedList"
                                :key="node.key"
                                :id="node.key"
                            >
                                <b-button
                                    variant="link"
                                    size="sm"
                                    class="btn-del btn-icon"
                                    @click.stop="deleteNode(node)"
                                >
                                    <i class="ti ti-xbox-x-filled"></i>
                                </b-button>
                                <div class="node-inner">
                                    <div
                                        class="tc-tree-item"
                                        :style="{
                                            marginLeft:
                                                (node.depth || 0) * 30 + 'px'
                                        }"
                                    >
                                        <!-- 보기 모드 -->
                                        <div
                                            v-if="!node._isEditing"
                                            class="tc-tree-list-info"
                                        >
                                            <div class="option">
                                                <strong class="name node-label"
                                                    >{{ node.metaFieldName }}
                                                </strong>
                                                <span class="operators">{{
                                                    node.extraValues
                                                        ?.operatorLabel ||
                                                    node.extraValues
                                                        ?.operator ||
                                                    ''
                                                }}</span>
                                                <span class="value">
                                                    {{
                                                        node.extraValues
                                                            ?.inputValue || ''
                                                    }}</span
                                                >
                                            </div>
                                            <div
                                                class="btn-updown-wrap updown-buttons"
                                            >
                                                <b-button
                                                    variant="outline-light-2"
                                                    size="xs"
                                                    class="btn-icon btn-edit"
                                                    @click.stop="
                                                        startEdit(node)
                                                    "
                                                >
                                                    <i class="ti ti-edit"></i>
                                                </b-button>
                                                <b-button
                                                    variant="light-2"
                                                    size="xs"
                                                    class="btn-icon"
                                                    v-if="canMoveUp(idx)"
                                                    @click.stop="moveUp(idx)"
                                                >
                                                    <i
                                                        class="ti ti-chevron-up"
                                                    ></i>
                                                </b-button>
                                                <b-button
                                                    variant="light-2"
                                                    size="xs"
                                                    class="btn-icon"
                                                    v-if="canMoveDown(idx)"
                                                    @click.stop="moveDown(idx)"
                                                >
                                                    <i
                                                        class="ti ti-chevron-down"
                                                    ></i>
                                                </b-button>
                                            </div>
                                        </div>

                                        <!-- 편집 모드 -->
                                        <div v-else class="tc-tree-list-edit">
                                            <strong class="name node-label">{{
                                                node.metaFieldName
                                            }}</strong>

                                            <!-- 타입 -->
                                            <b-form-select
                                                size="sm"
                                                v-model="
                                                    node.extraValues.inputType
                                                "
                                                @change="
                                                    (val) =>
                                                        updateExtra(
                                                            node.key,
                                                            'inputType',
                                                            val
                                                        )
                                                "
                                            >
                                                <b-form-select-option
                                                    v-for="ino in TARGET_INPUT_TYPE_OPTIONS"
                                                    :key="ino.value"
                                                    :value="ino.value"
                                                >
                                                    {{ ino.label }}
                                                </b-form-select-option>
                                            </b-form-select>

                                            <!-- 연산자 -->
                                            <b-form-select
                                                size="sm"
                                                v-model="
                                                    node.extraValues.operator
                                                "
                                                @change="
                                                    (val) =>
                                                        updateExtra(
                                                            node.key,
                                                            'operator',
                                                            val
                                                        )
                                                "
                                            >
                                                <b-form-select-option
                                                    v-for="op in TARGET_OPERATOR_OPTIONS[
                                                        node.extraValues
                                                            ?.inputType
                                                    ] || []"
                                                    :key="op.value"
                                                    :value="op.value"
                                                >
                                                    {{ op.label }}
                                                </b-form-select-option>
                                            </b-form-select>

                                            <!-- 값 -->
                                            <input
                                                v-model="
                                                    node.extraValues.inputValue
                                                "
                                                type="text"
                                                class="form-control form-control-sm"
                                                style="width: 150px"
                                                :placeholder="
                                                    setPlaceHolder(node)
                                                "
                                                :disabled="isBlocked(node.key)"
                                                @input="
                                                    (e) =>
                                                        updateExtra(
                                                            node.key,
                                                            'inputValue',
                                                            e.target.value
                                                        )
                                                "
                                            />

                                            <!-- 서브쿼리 / 관점설정 -->
                                            <b-button
                                                v-if="
                                                    inputTypeSelected[node.key]
                                                "
                                                @click="showSubQueryModal(node)"
                                                variant="light-2"
                                                size="sm"
                                                class="ms-auto"
                                            >
                                                서브쿼리
                                            </b-button>

                                            <b-button
                                                v-else-if="
                                                    !(
                                                        node.metaDimensionYn !==
                                                            'Y' &&
                                                        node.metaBidwDimensionYn !==
                                                            'Y'
                                                    )
                                                "
                                                @click="
                                                    showDimensionModal(node)
                                                "
                                                variant="light-2"
                                                size="sm"
                                                class="ms-auto"
                                            >
                                                관점설정
                                            </b-button>

                                            <b-button
                                                variant="soft-primary"
                                                size="sm"
                                                @click="applyEdit(node)"
                                            >
                                                <i class="ti ti-check"></i
                                                >수정완료
                                            </b-button>
                                            <b-button
                                                variant="light"
                                                size="sm"
                                                @click="cancelEdit(node)"
                                                >취소</b-button
                                            >
                                        </div>
                                    </div>
                                </div>
                                <!-- and/or 버튼은 각 노드 아래에 렌더링됩니다. 마지막 노드 아래에는 버튼을 표시하지 않습니다. -->
                                <div
                                    class="tc-tree-item"
                                    v-if="idx < flattenedList.length - 1"
                                    style="margin-top: 8px"
                                >
                                    <div
                                        class="btn-logic-wrap"
                                        :style="{
                                            marginLeft: getConnectorIndentPx(
                                                idx + 1
                                            )
                                        }"
                                    >
                                        <b-button
                                            variant="light-2"
                                            size="xs"
                                            @click="toggleCondition(idx + 1)"
                                        >
                                            {{ getConditionLabel(idx + 1) }}
                                        </b-button>

                                        <b-button
                                            variant="light-2"
                                            size="xs"
                                            class="btn-icon"
                                            @click.stop="moveLeft(idx + 1)"
                                        >
                                            <i
                                                class="ti ti-arrow-narrow-left"
                                            ></i>
                                        </b-button>
                                    </div>
                                </div>
                            </li>
                        </ul>
                    </div>
                    <!-- 설정전 드랍된 노드 -->
                    <div
                        class="tc-editor-wrapper"
                        @dragover.prevent
                        @drop="onDropToTargetConditionList"
                    >
                        <div
                            class="tc-editor"
                            v-if="
                                targetConditionList &&
                                targetConditionList.length > 0
                            "
                        >
                            <div class="tc-edit-list">
                                <div
                                    class="tc-edit-item"
                                    v-for="(item, index) in targetConditionList"
                                    :key="item.key"
                                    :data-id="item.key"
                                >
                                    <!-- 삭제 버튼 -->
                                    <b-button
                                        variant="link"
                                        size="sm"
                                        class="btn-del btn-icon"
                                        @click="deleteField(item, index)"
                                    >
                                        <i class="ti ti-xbox-x-filled"></i>
                                    </b-button>

                                    <!-- Label -->
                                    <label class="form-label mb-0 me-2">{{
                                        item.title
                                    }}</label>

                                    <!-- 타입 select -->
                                    <b-form-select
                                        size="sm"
                                        v-model="
                                            extraValues[item.key].inputType
                                        "
                                        @change="
                                            (val) =>
                                                updateExtra(
                                                    item.key,
                                                    'inputType',
                                                    val
                                                )
                                        "
                                    >
                                        <b-form-select-option
                                            v-for="ino in TARGET_INPUT_TYPE_OPTIONS"
                                            :key="ino.value"
                                            :value="ino.value"
                                            >{{
                                                ino.label
                                            }}</b-form-select-option
                                        >
                                    </b-form-select>

                                    <!-- operator select -->
                                    <b-form-select
                                        size="sm"
                                        v-model="extraValues[item.key].operator"
                                        @change="
                                            (val) =>
                                                updateExtra(
                                                    item.key,
                                                    'operator',
                                                    val
                                                )
                                        "
                                    >
                                        <b-form-select-option
                                            v-for="op in TARGET_OPERATOR_OPTIONS[
                                                extraValues[item.key]?.inputType
                                            ] || []"
                                            :key="op.value"
                                            :value="op.value"
                                            >{{
                                                op.label
                                            }}</b-form-select-option
                                        >
                                    </b-form-select>

                                    <!-- 값 입력 input -->
                                    <input
                                        type="text"
                                        class="form-control form-control-sm"
                                        v-model="
                                            extraValues[item.key].inputValue
                                        "
                                        @input="
                                            (e) =>
                                                updateExtra(
                                                    item.key,
                                                    'inputValue',
                                                    e.target.value
                                                )
                                        "
                                        :placeholder="setPlaceHolder(item)"
                                        :disabled="isBlocked(item.key)"
                                        style="width: 225px"
                                    />

                                    <!-- 서브쿼리 버튼 -->
                                    <b-button
                                        v-if="inputTypeSelected[item.key]"
                                        @click="showSubQueryModal(item)"
                                        variant="light-2"
                                        size="sm"
                                        class="ms-auto"
                                    >
                                        서브쿼리
                                    </b-button>

                                    <!-- 관점설정 버튼 -->
                                    <b-button
                                        v-else-if="
                                            !(
                                                item.metaDimensionYn !== 'Y' &&
                                                item.metaBidwDimensionYn !== 'Y'
                                            )
                                        "
                                        @click="showDimensionModal(item)"
                                        variant="light-2"
                                        size="sm"
                                        class="ms-auto"
                                    >
                                        관점설정
                                    </b-button>

                                    <!-- 설정 완료 버튼 -->
                                    <b-button
                                        variant="light-2"
                                        size="sm"
                                        class="ms-auto"
                                        @click="selectedField(item, index)"
                                    >
                                        설정 완료
                                    </b-button>
                                </div>
                            </div>
                        </div>
                        <!-- Dropzone -->
                        <Dropzone v-else>
                            타겟팅 조건을 설정할 관점을 끌어다 놓으세요.
                        </Dropzone>
                        <b-button
                            variant="light-2"
                            class="ms-auto"
                            @click="getFlatCompleteList()"
                        >
                            저장 데이터 확인
                        </b-button>

                        <b-button
                            variant="light-2"
                            class="ms-auto"
                            @click="checkCompleteListLoad()"
                        >
                            데이터 불러오기
                        </b-button>
                    </div>

                    <!-- 서브 쿼리 모달 -->
                    <b-modal
                        v-model="isSubQueryModalOpen"
                        title="서브쿼리 타게팅 조회"
                        hide-footer
                        centered
                        scrollable
                        size="xl"
                        @hidden="resetSubQueryModal"
                    >
                        <b-row class="table-header">
                            <b-col sm="auto" class="status">
                                <h5>
                                    전체 <span>{{ total }}</span
                                    >건
                                </h5>
                            </b-col>
                            <b-col cols="auto" class="ms-auto">
                                <b-form-checkbox
                                    switch
                                    inline
                                    v-model="subQueryMyTargetSwitch"
                                    @change="onSubQueryMyTargetSwitch"
                                >
                                    내 타겟팅 전체보기</b-form-checkbox
                                >
                            </b-col>
                        </b-row>
                        <Simplebar>
                            <table
                                class="table table-hover table-striped table-nowrap text-center"
                            >
                                <thead class="table-light">
                                    <tr>
                                        <th scope="col">No</th>
                                        <th scope="col">주제영역</th>
                                        <th scope="col">타겟 작업명</th>
                                        <th scope="col">타겟 아이디</th>
                                        <th scope="col">작업 유형</th>
                                        <th scope="col">진행 상태</th>
                                        <th scope="col">타겟 건수</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <tr
                                        v-for="(item, index) in subQueryList"
                                        :key="item.targetId"
                                        @click="selectSubQueryRow(item)"
                                        :class="{
                                            active:
                                                selectedSubQueryRow ===
                                                item.targetId
                                        }"
                                    >
                                        <td>{{ index + 1 }}</td>
                                        <td>{{ item.targetAreaName }}</td>
                                        <td>{{ item.targetName }}</td>
                                        <td>{{ item.targetId }}</td>
                                        <td>{{ item.executionType }}</td>
                                        <td>{{ item.executionStatus }}</td>
                                        <td>{{ item.executionCnt }}</td>
                                    </tr>
                                </tbody>
                            </table>
                        </Simplebar>
                        <Pager
                            :page="page"
                            :total="total"
                            @update:page="page = $event"
                        />
                        <template #footer>
                            <div
                                class="d-flex flex-wrap gap-2 justify-content-center"
                            >
                                <b-button
                                    variant="light"
                                    @click="cancelSubQueryModal"
                                    >닫기</b-button
                                >
                                <b-button
                                    variant="primary"
                                    @click="confirmSubQueryModal"
                                    >확인</b-button
                                >
                            </div>
                        </template>
                    </b-modal>

                    <!-- 관점 설정 모달 -->
                    <b-modal
                        v-model="isDemensionModalOpen"
                        title="관점 설정"
                        centered
                        scrollable
                        size="lg"
                    >
                        <b-row class="g-3">
                            <b-col cols="5">
                                <div
                                    class="d-flex justify-content-between mb-2"
                                >
                                    <strong>관점 값</strong>
                                    <small
                                        >{{
                                            availableDimensions.length
                                        }}개</small
                                    >
                                </div>
                                <b-form-select
                                    multiple
                                    :options="
                                        availableDimensions.map((d) => ({
                                            value: String(d.metaDimensionId),
                                            text: d.metaDimensionName
                                        }))
                                    "
                                    v-model="selectedAvailableIds"
                                    style="height: 260px"
                                />
                            </b-col>
                            <b-col
                                cols="2"
                                class="d-flex flex-column justify-content-center align-items-center gap-2"
                            >
                                <b-button
                                    size="sm"
                                    variant="light-2"
                                    class="w-75"
                                    @click="moveAllToChosen"
                                    >&gt;&gt;</b-button
                                >
                                <b-button
                                    size="sm"
                                    variant="light-2"
                                    class="w-75"
                                    @click="moveSelectedToChosen"
                                    >&gt;</b-button
                                >
                                <b-button
                                    size="sm"
                                    variant="light-2"
                                    class="w-75"
                                    @click="moveSelectedToAvailable"
                                    >&lt;</b-button
                                >
                                <b-button
                                    size="sm"
                                    variant="light-2"
                                    class="w-75"
                                    @click="moveAllToAvailable"
                                    >&lt;&lt;</b-button
                                >
                            </b-col>
                            <b-col cols="5">
                                <div
                                    class="d-flex justify-content-between mb-2"
                                >
                                    <strong>선택된 관점 값</strong>
                                    <small
                                        >{{
                                            chosenDimensionsForCurrent.length
                                        }}개</small
                                    >
                                </div>
                                <b-form-select
                                    multiple
                                    :options="
                                        chosenDimensionsForCurrent.map((d) => ({
                                            value: String(d.metaDimensionId),
                                            text: d.metaDimensionName
                                        }))
                                    "
                                    v-model="selectedChosenIds"
                                    style="height: 260px"
                                />
                            </b-col>
                        </b-row>

                        <template #footer>
                            <div class="d-flex justify-content-end w-100 gap-2">
                                <b-button
                                    variant="light"
                                    @click="cancelDimensionModal"
                                    >취소</b-button
                                >
                                <b-button
                                    variant="primary"
                                    @click="confirmDimensionModal"
                                    >확인</b-button
                                >
                            </div>
                        </template>
                    </b-modal>

                    <!-- Footer -->
                    <template #footer>
                        <h4 class="card-title">타겟팅 필수 조건</h4>
                        <b-FormGroup
                            class="form-check-primary hstack gap-3"
                            v-if="
                                targetAutoConditionList &&
                                targetAutoConditionList.length > 0
                            "
                            v-for="item in targetAutoConditionList"
                        >
                            <b-FormCheckbox
                                v-model="targetingConditionCheckeds"
                                :key="item.targetId"
                                :value="item.targetId"
                                disabled
                            >
                                {{ item.targetName }}
                            </b-FormCheckbox>
                        </b-FormGroup>
                    </template>
                </b-card>
            </b-col>

            <b-col>
                <!-- Card: 출력 조건 -->
                <b-card
                    class="tc-output"
                    header-class="d-flex align-items-end gap-2"
                >
                    <template #header>
                        <h4 class="card-title mb-0">출력 조건</h4>
                        <p class="card-subtitle text-muted">
                            <strong class="text-info">{{
                                targetReportList.length
                            }}</strong
                            >개의 출력조건이 추가되었습니다.
                        </p>
                        <b-button
                            variant="light-2"
                            class="ms-auto"
                            @click="resetTargetReportList()"
                        >
                            <i class="ti ti-refresh"></i>조건 초기화
                        </b-button>
                    </template>

                    <div
                        class="chip-draggable-wrapper"
                        @dragover.prevent
                        @drop="onDropToTargetReportList"
                    >
                        <Simplebar
                            v-if="
                                targetReportList && targetReportList.length > 0
                            "
                        >
                            <Draggable
                                :list="targetReportList"
                                item-key="key"
                                class="chip-draggable"
                                handle=".chip-handle"
                            >
                                <template #item="{ element }">
                                    <div class="chip">
                                        <i
                                            class="ti ti-grip-vertical chip-handle"
                                        ></i>
                                        <span class="chip-label">{{
                                            element.label ??
                                            element.title ??
                                            element.key
                                        }}</span>

                                        <b-button
                                            size="xs"
                                            variant="outline-light"
                                            :class="[
                                                'btn-icon btn-edit-function',
                                                {
                                                    active:
                                                        !!element.funcName ||
                                                        (outputFunctionSaveData &&
                                                            outputFunctionSaveData[
                                                                element.key
                                                            ] &&
                                                            outputFunctionSaveData[
                                                                element.key
                                                            ].chip &&
                                                            outputFunctionSaveData[
                                                                element.key
                                                            ].chip.key ===
                                                                element.key)
                                                }
                                            ]"
                                            @click="
                                                showOutputFunctionModal({
                                                    funcName:
                                                        element.funcName ||
                                                        'date_format',
                                                    chip: element
                                                })
                                            "
                                        >
                                            <img
                                                src="@/assets/images/svg/function.svg"
                                                height="10"
                                            />
                                        </b-button>

                                        <b-button
                                            size="xs"
                                            variant="link"
                                            class="btn-icon btn-chip-del"
                                            @click="
                                                deleteOutputFunctionRow(element)
                                            "
                                        >
                                            <i class="ti ti-x"></i>
                                        </b-button>
                                    </div>
                                </template>
                            </Draggable>
                        </Simplebar>
                        <Dropzone style="min-height: 100px" v-else
                            >데이터를 출력할 관점을 끌어다 놓으세요.</Dropzone
                        >
                    </div>
                </b-card>
            </b-col>
        </b-row>
    </Simplebar>
    <!-- Modal: 출력함수 설정 -->
    <b-modal
        v-model="isOutputFunctionModalOpen"
        title="출력함수 설정"
        centered
        scrollable
        size="lg"
        @hidden="resetCaseParamPairs"
    >
        <b-row class="row-cols-1 row-cols-lg-2 g-3 function-setting">
            <b-col>
                <Simplebar style="max-height: 300px">
                    <b-list-group class="function-list">
                        <b-list-group-item
                            v-for="func in outputFunctionList"
                            :key="func.targetFunctionId"
                            :active="
                                selectedOutputFunctionRow &&
                                String(
                                    selectedOutputFunctionRow.targetFunctionId
                                ) === String(func.targetFunctionId)
                            "
                            action
                            @click="selectedOutputFunction(func)"
                        >
                            <strong>{{ func.targetFunctionName }}</strong>
                            <span>{{ func.targetFunctionNameKo }}</span>
                        </b-list-group-item>
                    </b-list-group>
                </Simplebar>
            </b-col>
            <!-- 함수 상세 -->
            <b-col v-if="selectedOutputFunctionRow">
                <b-card class="function-detail">
                    <h4>
                        {{ selectedOutputFunctionRow.targetFunctionComment1 }}
                    </h4>
                    <p class="text-muted">
                        {{ selectedOutputFunctionRow.targetFunctionComment2 }}
                    </p>
                    <p class="text-primary">
                        {{ selectedOutputFunctionRow.targetFunctionComment3 }}
                    </p>
                </b-card>

                <!-- 인수 입력 -->
                <b-form>
                    <div class="mb-2">
                        <div class="input-group">
                            <div class="input-group-text">인수 1</div>
                            <b-form-input
                                v-model="outputFunctionParamValues[0]"
                                type="text"
                                disabled
                            />
                        </div>
                    </div>
                    <!-- ✅ 일반 함수 전용 (case 제외) -->
                    <template v-if="!isCaseLikeSelected">
                        <div
                            v-for="n in outputFunctionParamInputCount"
                            :key="n"
                            class="mb-2"
                        >
                            <div class="input-group">
                                <div class="input-group-text">
                                    {{
                                        getParamLabel(
                                            selectedOutputFunctionRow.targetFunctionName,
                                            n
                                        )
                                    }}
                                </div>
                                <b-form-input
                                    v-model="outputFunctionParamValues[n]"
                                    type="text"
                                />
                            </div>
                        </div>
                    </template>
                    <template v-else>
                        <div
                            v-for="(pair, pIdx) in caseParamPairs || []"
                            :key="pIdx"
                            class="mb-2 gap-2 hstack"
                        >
                            <h6 class="mb-0 me-1 text-end" style="width: 50px">
                                {{ pIdx + 1 }}
                            </h6>
                            <div class="input-group">
                                <div class="input-group-text">조건</div>
                                <b-form-input
                                    v-model="pair.condition"
                                    type="text"
                                />
                            </div>
                            <div class="input-group">
                                <div class="input-group-text">결과</div>
                                <b-form-input
                                    v-model="pair.result"
                                    type="text"
                                />
                            </div>
                        </div>

                        <b-button variant="light" @click="addCasePair"
                            >+ 조건 추가</b-button
                        >
                    </template>
                </b-form>
            </b-col>
        </b-row>
        <template #footer>
            <b-button
                variant="outline-danger"
                class="me-auto"
                @click="deleteOutputFunction"
            >
                <i class="ti ti-trash"></i> 제거
            </b-button>
            <b-button variant="light" @click="isOutputFunctionModalOpen = false"
                >취소</b-button
            >
            <b-button variant="primary" @click="saveOutputFunction"
                >저장</b-button
            >
        </template>
    </b-modal>
    <!-- 타겟팅 목적 팝업 -->
    <b-modal
        v-model="isTargetGroupModalOpen"
        hide-footer
        centered
        scrollable
        size="lg"
        class="target-group-modal"
        header-class="align-items-start"
        footer-class="d-flex flex-wrap justify-content-between gap-2"
    >
        <!-- Header -->
        <template #title>
            <h3 class="mb-1">
                주제영역을 선택하기 위해 아래 사용 목적을 선택해주세요.
            </h3>
            <p class="text-muted fs-13 mb-0">
                작업 유형 선택 시 해당 목적에 맞는 주제영역이 필터링됩니다.
            </p>
        </template>

        <!-- Body -->
        <TargetGroupSelector
            :target-area-group="targetAreaGroup"
            :selected-target-area-group="selectedTargetAreaGroup"
            :cols="{ cols: 12, sm: 6, xl: 4 }"
            @select="targetAreaGroupSelectedModal"
        />

        <!-- Footer -->
        <template #footer>
            <!-- 왼쪽: 설명문 -->
            <div class="purpose-desc help-message">
                <template
                    v-if="selectedTargetAreaGroup"
                    v-html="selectedTargetAreaGroup"
                >
                    <i class="ti ti-info-circle"></i>
                    <div
                        v-html="selectedTargetAreaGroup.targetAreaGroupNote"
                    ></div>
                    <!-- {{ selectedTargetAreaGroup.description }} -->
                </template>
                <template v-else>
                    목적을 선택하면 상세 설명이 표시됩니다.
                </template>
            </div>

            <!-- 오른쪽: 버튼 -->
            <div class="d-flex gap-2 ms-auto">
                <b-button
                    variant="light"
                    @click="isTargetGroupModalOpen = false"
                >
                    취소
                </b-button>
                <b-button
                    variant="primary"
                    @click="confirmTargetGroupSelection"
                    :disabled="!selectedTargetAreaGroup"
                >
                    선택 완료
                </b-button>
            </div>
        </template>
    </b-modal>
</template>
<script setup>
// ============================================================
// 구성요소: ExpertQueryMain
// 역할: 타겟팅 조건/출력 필드 빌더 및 미리보기 관리
// 주석 규칙: 섹션 헤더(====), 함수 JSDoc(/** */), 인라인 설명(//)
// ============================================================

// [Imports] 컴포넌트/유틸/코드 상수
import {
    ref,
    reactive,
    nextTick,
    computed,
    onMounted,
    onBeforeUnmount,
    watch,
    watchEffect,
    toRaw
} from 'vue'
import Dropzone from '@/components/Dropzone.vue'
import Simplebar from 'simplebar-vue'
import AntTree from '@/components/expert/AntTree.vue'
import Draggable from 'vuedraggable'
import EmptyMessage from '@/components/EmptyMessage.vue'
import ExpertPerspectiveCollectionModal from '@/components/expert/ExpertPerspectiveCollectionModal.vue'
import {
    TARGET_OPERATOR_OPTIONS,
    TARGET_TYPE_VIEW_MAP,
    TARGET_INPUT_TYPE_OPTIONS
} from '@/utils/expertCodes'
import * as expertModules from '@/modules/expert'
import Pager from '@/components/Pager.vue'
import { showAlert, showConfirm } from '@/utils/common'
import TargetGroupSelector from '@/components/expert/TargetGroupSelector.vue'
import { useExpertStore } from '@/store/expert.js'
import { storeToRefs } from 'pinia'

// 디버그 플래그 (배포용에서는 false 권장)
const DEBUG_TOGGLE = true

const chips = ref([])
const pagingState = reactive({})

const isTargetGroupModalOpen = ref(false) // 목적 list 모달 on/off
const targetAreaGroup = ref([]) // 목적 그룹

const targetAreaList = ref([]) // 주제영역 list
const selectedTargetGroupArea = ref(null) // 선택한 주제영역
const selectedTargetAreaId = ref(null) // 선택한 주제영역 ID

const metaTableList = ref([])

const homeSearchParam = ref({
    homeReqestType: '',
    homeSearchSimulation: '',
    loginId: '',
    regDate: '',
    changDate: '',
    regId: '',
    changId: '',
    baseDate: '',
    targetId: '',
    totalCount: 0,
    showRowSize: 0,
    currentPageIdx: 0,
    start: 0,
    end: 0,
    page: 0,
    listRows: 0,
    pageRows: 0
})
// 목적 list select & 모달 띄우기
const showTargetGroupModal = async () => {
    const response = await expertModules.selectTargetAreaGroup(
        homeSearchParam.value
    )
    targetAreaGroup.value = response.selectTargetAreaGroup
    // 불러오기 이후 현재 선택된 그룹을 모달에서도 active로 표시
    try {
        const preferredGroupId =
            selectedTargetGroupArea.value?.targetAreaGroupId ||
            response?.selectTargetAreaGroupId ||
            null
        selectedTargetAreaGroup.value =
            (Array.isArray(targetAreaGroup.value)
                ? targetAreaGroup.value.find(
                      (g) => g.targetAreaGroupId === preferredGroupId
                  )
                : null) ||
            targetAreaGroup.value?.[0] ||
            null
    } catch (e) {
        // 방어적 처리: 문제가 있어도 모달은 열리도록 함
        selectedTargetAreaGroup.value = targetAreaGroup.value?.[0] || null
    }
    isTargetGroupModalOpen.value = true
}

// 퍼블리싱 추가
const selectedTargetAreaGroup = ref(null)

function targetAreaGroupSelectedModal(item) {
    selectedTargetAreaGroup.value = item
}

const confirmTargetGroupSelection = () => {
    if (!selectedTargetAreaGroup.value) return
    const id = selectedTargetAreaGroup.value.targetAreaGroupId
    targetAreaGroupSelected(id)
    isTargetGroupModalOpen.value = false
}

const expertSearchParam = ref({
    selectTargetAreaGroupId: '',
    selectTargetAreaId: '',
    selectTargetId: '',
    selectUserId: '',
    expertReqestType: ''
})

// 목적 선택
async function targetAreaGroupSelected(targetAreaGroupId) {
    expertSearchParam.value.selectTargetAreaGroupId = targetAreaGroupId
    const response = await expertModules.selectTargetAreaList(
        expertSearchParam.value
    )
    if (response) {
        targetAreaList.value = response.selectTargetAreaList
        if (targetAreaList.value && targetAreaList.value.length > 0) {
            selectedTargetAreaId.value = targetAreaList.value[0].targetAreaId
            selectedTargetGroupArea.value =
                response.selectTargetAreaGroupList[0]
            targetAreaSelected(selectedTargetAreaId.value)
            setDefault()
        } else {
            selectedTargetAreaId.value = null
        }
    }
}

const jsTreeModel = ref({
    targetAreaId: '',
    empNo: ''
})
const targetModel = ref({
    targetAreaId: ''
})
// 타겟팅 필수 조건 list
const targetAutoConditionList = ref([])
// 타겟팅 필수 조건 checkbox
const targetingConditionCheckeds = ref([])

// 주제 선택
const targetAreaSelected = async (targetAreaId) => {
    jsTreeModel.value.targetAreaId = targetAreaId
    const response = await expertModules.selectTreeRootItemTest(
        jsTreeModel.value
    )
    targetModel.value.targetAreaId = targetAreaId
    const responseCon = await expertModules.selectTargetAutoCondition(
        targetModel.value
    )
    if (response) {
        setDefault()
        nextTick(() => {
            metaTableList.value = response.selectTreeItem
        })
    }
    targetAutoConditionList.value = responseCon.targetAutoConditionList
    // 기본적으로 필수 조건은 모두 체크 상태로 초기화합니다. (v-model이 체크 상태를 제어함)
    try {
        if (
            Array.isArray(responseCon.targetAutoConditionList) &&
            responseCon.targetAutoConditionList.length > 0
        ) {
            targetingConditionCheckeds.value =
                responseCon.targetAutoConditionList.map((it) => it.targetId)
        } else {
            targetingConditionCheckeds.value = []
        }
    } catch (e) {
        console.warn(
            '[targetAreaSelected] targetingCondition 초기화 중 오류',
            e
        )
    }
    if (DEBUG_TOGGLE)
        console.debug(
            '[targetAreaSelected] targetAutoConditionList',
            responseCon.targetAutoConditionList
        )
}

const store = useExpertStore()
const { selectedTargetGroupId, moveToParam } = storeToRefs(store)

onMounted(async () => {
    targetingConditionCheckeds.value = targetAutoConditionList.value.map(
        (t) => t.targetId
    )
    const response = await expertModules.selectTargetAreaGroup(
        homeSearchParam.value
    )
    targetAreaGroup.value = response.selectTargetAreaGroup
})

watch(
    () => selectedTargetGroupId,
    (newVal) => {
        if (newVal) {
            targetAreaGroupSelected(newVal)
        }
    },
    { immediate: true }
)
// ============================================================
// 섹션: Drag & Drop (조건/출력 빌더)
// ============================================================
const draggedNode = ref(null) // 드래그 되는 node
const targetConditionList = ref([]) // 타겟팅 조건 드랍 list
const targetReportList = ref([]) // 출력 조건 드랍 list
const extraValues = reactive({}) // 쿼리 비교 조건

// 트리 list 에서 드래그 start
/** 드래그 시작: 트리 항목을 조건/출력 영역으로 이동 준비
 * @param {Object} node 드래그한 트리 노드
 * @param {DragEvent} event 원본 드래그 이벤트
 */
function onDragStart(node, event) {
    draggedNode.value = node
    event.dataTransfer.setData('text/plain', node.key)
}

// 드래그 노드 타겟팅 조건에 드랍
/** 드롭(조건): 드래그한 항목을 조건 빌더에 추가 */
function onDropToTargetConditionList() {
    if (draggedNode.value) {
        // ✅ 새 key 생성 (timestamp 기반 또는 uuid)
        const newKey = draggedNode.value.key + '_' + Date.now()
        if (!extraValues[newKey]) {
            extraValues[newKey] = {
                operator: 'A1',
                operatorLabel: '동등 (=)',
                inputValue: '',
                inputType: '1',
                inputTypeLabel: '직접입력'
            }
        }
        // ✅ 리스트에 추가
        targetConditionList.value.push({
            ...draggedNode.value,
            key: newKey,
            extraValues: extraValues[newKey],
            depth: 0,
            _isEditing: false,
            _backup: null
        })
        draggedNode.value = null
    }
}

// 타겟팅 조건 삭제
/** 조건 빌더 항목 삭제
 * @param {Object} item 대상 항목
 * @param {number} index 인덱스
 */
function deleteField(item, index) {
    targetConditionList.value.splice(index, 1)
    delete extraValues[item.key]
}

// 타겟팅 조건 입력 필드
const inputTypeSelected = reactive({})

// 타겟팅 조건 편집
/** 옵션에서 레이블 찾기
 * @param {Array<{value:any,label:string}>} options 옵션 목록
 * @param {any} value 선택 값
 * @returns {string}
 */
function findLabelFromOptions(options, value) {
    const found = (options || []).find((opt) => opt.value === value)
    return found ? found.label : value
}

/** 서버 연산자 문자열을 내부 코드(A1/B1...)로 매핑 */
function mapServerOperatorToCode(opRaw, inputType = '1') {
    if (!opRaw) return inputType === '3' ? 'B1' : 'A1'
    const op = String(opRaw).toUpperCase().trim()
    // 기본 비교 연산자
    const cmpMap = {
        '=': 'A1',
        '==': 'A1',
        '<>': 'A2',
        '!=': 'A2',
        '>': 'A3',
        '>=': 'A4',
        '<': 'A5',
        '<=': 'A6'
    }
    const setMap = {
        IN: 'B1',
        'NOT IN': 'B2'
    }
    // LIKE 류는 서버에서 패턴을 나눠주지 않는 한 일반 비교로 처리
    if (setMap[op]) return setMap[op]
    if (cmpMap[op]) return cmpMap[op]
    return inputType === '3' ? 'B1' : 'A1'
}

/** 내부 코드에 맞는 라벨 계산 */
function getOperatorLabelByCode(code, inputType = '1') {
    const opts = TARGET_OPERATOR_OPTIONS[inputType] || []
    const found = opts.find((o) => o.value === code)
    return found ? found.label : code
}

/** 추가값 업데이트: inputType/operator/inputValue 등 동기화
 * @param {string} key 노드 키
 * @param {'inputType'|'operator'|'inputValue'} field 변경 필드
 * @param {any} rawValue 이벤트/값
 */
function updateExtra(key, field, rawValue) {
    // 1) 재귀 탐색기: completeList에는 중첩된 그룹 객체가 포함될 수 있음
    const findNodeRecursive = (arr) => {
        if (!Array.isArray(arr)) return null
        for (let i = 0; i < arr.length; i++) {
            const n = arr[i]
            if (!n) continue
            if (n.key === key) return { parent: arr, idx: i, node: n }
            // 그룹 컨테이너
            if (Array.isArray(n.group)) {
                // group 배열을 검사
                const res = findNodeRecursive(n.group)
                if (res) return res
            }
        }
        return null
    }

    let found = findNodeRecursive(completeList.value)
    let listRef = completeList.value
    let idx = -1
    let node = null
    if (!found) {
        // 대체: targetConditionList(평면 배열)에서 탐색
        const i = targetConditionList.value.findIndex((n) => n.key === key)
        if (i !== -1) {
            listRef = targetConditionList.value
            idx = i
            node = listRef[idx]
        }
    } else {
        listRef = found.parent
        idx = found.idx
        node = found.node
    }
    if (!node) return

    // 2) node.extraValues가 전역 extraValues 맵과 연결되어 있는지 보장
    if (!node.extraValues) {
        node.extraValues =
            extraValues[key] ??
            (extraValues[key] = {
                inputType: '1',
                inputTypeLabel: '직접입력',
                operator: 'A1',
                operatorLabel: '동등 (=)',
                inputValue: ''
            })
    } else {
        if (!extraValues[key]) extraValues[key] = node.extraValues
    }

    const ex = node.extraValues

    // 3) 이벤트 payload 정규화
    const value = rawValue && rawValue.target ? rawValue.target.value : rawValue

    // 4) 참조를 보존하기 위해 제자리(mutating) 수정
    if (field === 'inputType') {
        const isSubQuery = value === '3'
        ex.inputType = value
        ex.inputTypeLabel = findLabelFromOptions(
            TARGET_INPUT_TYPE_OPTIONS,
            value
        )
        ex.operator = isSubQuery ? 'B1' : 'A1'
        ex.operatorLabel = findLabelFromOptions(
            TARGET_OPERATOR_OPTIONS[ex.inputType] || [],
            ex.operator
        )
        ex.inputValue = '' // 타입 바뀌면 값 초기화
        inputTypeSelected[key] = isSubQuery
    } else if (field === 'operator') {
        ex.operator = value
        ex.operatorLabel = findLabelFromOptions(
            TARGET_OPERATOR_OPTIONS[ex.inputType] || [],
            value
        )
    } else if (field === 'inputValue') {
        ex.inputValue = value
    }

    // 5) 필요 시 최상위 배열에 대해 반응성 트리거
    // 노드가 completeList의 직계 자식(최상위)인 경우, 교체하여 반응성을 보장
    if (listRef === completeList.value) {
        // 부모 completeList에서 실제 인덱스 찾기(중첩 시 달라질 수 있음)
        const topIdx = listRef.findIndex((n) => n === node)
        if (topIdx !== -1) {
            completeList.value.splice(topIdx, 1, {
                ...node,
                extraValues: { ...ex }
            })
        }
    }
}

// 타겟팅 조건 변경시 입력 필드 값 변경
/** 입력 placeholder 결정: 타입/차원 여부에 따라 가이드 반환 */
function setPlaceHolder(item) {
    if (inputTypeSelected[item.key]) {
        return TARGET_TYPE_VIEW_MAP.find((t) => t.value == 'inputGuideSubQuery')
            ?.label
    } else if (item.metaDimensionYn === 'Y') {
        return TARGET_TYPE_VIEW_MAP.find(
            (t) => t.value == 'inputGuideDimension'
        )?.label
    } else if (item.metaBidwDimensionYn === 'Y') {
        return TARGET_TYPE_VIEW_MAP.find(
            (t) => t.value == 'inputGuideDimension'
        )?.label
    } else if (item.metaFieldDataType === 'string') {
        return TARGET_TYPE_VIEW_MAP.find((t) => t.value == 'inputGuideString')
            ?.label
    } else if (item.metaFieldDataType === 'double') {
        return TARGET_TYPE_VIEW_MAP.find((t) => t.value == 'inputGuideDouble')
            ?.label
    } else if (item.metaFieldDataType === 'timestamp') {
        return TARGET_TYPE_VIEW_MAP.find(
            (t) => t.value == 'inputGuideTimestamp'
        )?.label
    } else if (item.metaFieldDataType === 'date') {
        return TARGET_TYPE_VIEW_MAP.find(
            (t) => t.value == 'inputGuideTimestamp'
        )?.label
    } else {
        return TARGET_TYPE_VIEW_MAP.find(
            (t) => t.value == 'inputGuideEmptyValue'
        )?.label
    }
    TARGET_TYPE_VIEW_MAP
}

// 서브 쿼리 선택시 입력 필드 block
/** 서브쿼리 선택 시 수동 입력 차단 여부 */
function isBlocked(key) {
    return inputTypeSelected[key]
}

// ============================================================
// 섹션: 서브쿼리 선택 모달
// ============================================================
const isSubQueryModalOpen = ref(false) // 서브 쿼리 모달 on/off
const subQueryList = ref([])
const subQueryInputTargetId = ref({})
const subQueryMyTargetSwitch = ref(false)
const selectedSubQueryRow = ref(null)
const selectedSubQueryItem = ref(null)
const selectedSubQueryTargetId = ref({})

// 페이지 상태
const page = ref(1)
const total = ref(0)

// 서브 쿼리 모달 param
const targetSubQueryModel = ref({
    metaFieldId: '',
    regId: '',
    searchType: '',
    showRowSize: '',
    currentPageIdx: '',
    showRowSize: ''
})

// 서브 쿼리 모달 열기
/** 서브쿼리 모달 표시: 항목 선택 > 목록 조회 후 모달 오픈 */
const showSubQueryModal = async (item) => {
    const response = await expertModules.selectTargetSubQuery(
        targetSubQueryModel.value
    )
    if (response) {
        subQueryList.value = response.targetSubQueryList
        total.value = response.total
        isSubQueryModalOpen.value = true
        subQueryInputTargetId.value.key = item.key
    }
}
// ✅ 리스트 클릭시 → 선택만 표시 (즉시 반영 X)
/** 서브쿼리 행 선택(일시 저장, DB 저장 아님) */
const selectSubQueryRow = (item) => {
    selectedSubQueryRow.value = item.targetId
    selectedSubQueryItem.value = item
}

// ✅ OK 버튼 클릭시 → 실제 반영
/** 서브쿼리 확정: 선택값을 해당 노드 inputValue로 반영 */
const confirmSubQueryModal = () => {
    if (!selectedSubQueryItem.value) {
        showAlert('항목을 선택해주세요.', '', 'warning')
        return
    }

    const key = subQueryInputTargetId.value.key
    updateExtra(key, 'inputValue', selectedSubQueryItem.value.targetId)

    // operator, operatorLabel도 같이 세팅
    updateExtra(key, 'operator', 'B1')

    isSubQueryModalOpen.value = false
    resetSubQueryModal()
}

// ✅ Cancel 버튼 → 아무것도 반영 안함
/** 서브쿼리 취소: 변경 없이 모달 닫기 */
const cancelSubQueryModal = () => {
    isSubQueryModalOpen.value = false
    resetSubQueryModal()
}

// ✅ 모달 닫힐 때 초기화
/** 서브쿼리 모달 상태 초기화 */
const resetSubQueryModal = () => {
    subQueryList.value = []
    total.value = 0
    subQueryMyTargetSwitch.value = false
    subQueryInputTargetId.value = {}
    selectedSubQueryRow.value = null
    selectedSubQueryItem.value = null
    selectedSubQueryTargetId.value = {}
    targetSubQueryModel.value = {
        metaFieldId: '',
        regId: '',
        searchType: '',
        showRowSize: '',
        currentPageIdx: ''
    }
}

// 서브 쿼리 모달 swith
/** 내 타겟만 보기 스위치 토글 처리 */
const onSubQueryMyTargetSwitch = async () => {
    if (subQueryMyTargetSwitch.value) {
        targetSubQueryModel.value.searchType = 'all'
    } else {
        targetSubQueryModel.value.searchType = ''
    }

    const response = await expertModules.selectTargetSubQuery(
        targetSubQueryModel.value
    )
    if (response) {
        if (DEBUG_TOGGLE) console.debug('selectTargetswitchSubQuery', response)
        subQueryList.value = response.targetSubQueryList
        total.value = response.total
    }
}

// ============================================================
// 섹션: 디멘전(차원) 선택 모달
// ============================================================
const isDemensionModalOpen = ref(false) // 관점 설정 모달 on/off
const dimensionList = ref([]) // 관점 설정 list
const currentDimensionKey = ref('') // 현재 모달을 연 항목의 key
const currentDimensionItem = ref(null) // 현재 모달을 연 항목 객체
const chosenDimensionsMap = reactive({}) // key 별 선택된 관점 값 목록
const selectedAvailableIds = ref([]) // 좌측(가용) 선택된 항목 ID 목록
const selectedChosenIds = ref([]) // 우측(선택됨) 선택된 항목 ID 목록

// 현재 항목 기준 선택된 관점 목록
const chosenDimensionsForCurrent = computed(() => {
    const key = currentDimensionKey.value
    return Array.isArray(chosenDimensionsMap[key])
        ? chosenDimensionsMap[key]
        : []
})

// 좌측(가용) 목록 = 전체 - 선택됨
const availableDimensions = computed(() => {
    const chosen = new Set(
        chosenDimensionsForCurrent.value.map((d) => String(d.metaDimensionId))
    )
    return (dimensionList.value || []).filter(
        (d) => !chosen.has(String(d.metaDimensionId))
    )
})

// 관점 설정 list select & 모달 열기
const dimensionParam = ref({
    total: 0,
    showRowSize: 0,
    currentPageIdx: 0,
    start: 0,
    end: 0,
    metaFieldId: '',
    metaItgCd: '',
    metaItgNm: '',
    dimensionSearchWord: ''
})

/** 디멘전(차원) 목록 조회 후 모달 표시 */
const showDimensionModal = async (item) => {
    dimensionParam.value.metaFieldId = item.metaFieldId
    currentDimensionKey.value = item.key
    currentDimensionItem.value = item
    const response = await expertModules.selectDimensionList(
        dimensionParam.value
    )
    if (response) {
        dimensionList.value = response.dimensionList
        if (DEBUG_TOGGLE) console.debug('selectDimensionList', response)
        // 기존 저장값이 있으면 초기화
        initChosenForItem(item)
        // 선택 초기화
        selectedAvailableIds.value = []
        selectedChosenIds.value = []
        isDemensionModalOpen.value = true
    }
}

/** 현재 아이템에 대해 기존 선택값이 있으면 복원 */
function initChosenForItem(item) {
    const key = item?.key
    if (!key) return
    if (!Array.isArray(chosenDimensionsMap[key])) {
        chosenDimensionsMap[key] = []
    }
    // extraValues에 dimensionIds가 저장되어 있으면 이를 기준으로 복원
    const ex = extraValues[key] || {}
    const idsStr = ex.dimensionIds || ''
    if (idsStr) {
        const idSet = new Set(idsStr.split(',').map((s) => s.trim()))
        const restored = (dimensionList.value || []).filter((d) =>
            idSet.has(String(d.metaDimensionId))
        )
        chosenDimensionsMap[key] = restored
    }
}

/** 좌측 선택 항목을 우측으로 이동 */
function moveSelectedToChosen() {
    const key = currentDimensionKey.value
    if (!key) return
    if (!Array.isArray(chosenDimensionsMap[key])) {
        chosenDimensionsMap[key] = []
    }
    const toAddSet = new Set(selectedAvailableIds.value.map(String))
    const toAdd = availableDimensions.value.filter((d) =>
        toAddSet.has(String(d.metaDimensionId))
    )
    const existing = new Map(
        chosenDimensionsMap[key].map((d) => [String(d.metaDimensionId), d])
    )
    toAdd.forEach((d) => existing.set(String(d.metaDimensionId), d))
    chosenDimensionsMap[key] = Array.from(existing.values())
    selectedAvailableIds.value = []
}

/** 좌측 전체를 우측으로 이동 */
function moveAllToChosen() {
    const key = currentDimensionKey.value
    if (!key) return
    chosenDimensionsMap[key] = [...(dimensionList.value || [])]
    selectedAvailableIds.value = []
}

/** 우측 선택 항목을 좌측으로 이동(=우측에서 제거) */
function moveSelectedToAvailable() {
    const key = currentDimensionKey.value
    if (!key) return
    const removeSet = new Set(selectedChosenIds.value.map(String))
    chosenDimensionsMap[key] = chosenDimensionsForCurrent.value.filter(
        (d) => !removeSet.has(String(d.metaDimensionId))
    )
    selectedChosenIds.value = []
}

/** 우측 전체 제거 */
function moveAllToAvailable() {
    const key = currentDimensionKey.value
    if (!key) return
    chosenDimensionsMap[key] = []
    selectedChosenIds.value = []
}

/** 모달 확인: 선택값을 현재 노드의 extraValues에 반영 */
function confirmDimensionModal() {
    const key = currentDimensionKey.value
    if (!key) {
        isDemensionModalOpen.value = false
        return
    }
    const selected = chosenDimensionsForCurrent.value
    const names = selected.map((d) => d.metaDimensionName).join(',')
    const ids = selected.map((d) => d.metaDimensionId).join(',')

    // 값/연산자 반영
    updateExtra(key, 'inputValue', names)

    // 선택 개수에 따른 연산자 보정
    const ex = extraValues[key] || {}
    if (selected.length > 1) {
        updateExtra(key, 'operator', 'B1') // IN
    } else if (selected.length === 1) {
        if (ex.operator === 'B7' || ex.operator === 'B8') {
            updateExtra(key, 'operator', 'A1') // =
        }
    }

    // 선택된 ID들을 보존(추후 서버로 보낼 때 사용 가능)
    if (!extraValues[key]) extraValues[key] = {}
    extraValues[key].dimensionIds = ids

    // 닫기 및 선택 초기화
    isDemensionModalOpen.value = false
    selectedAvailableIds.value = []
    selectedChosenIds.value = []
}

/** 모달 취소 */
function cancelDimensionModal() {
    isDemensionModalOpen.value = false
    selectedAvailableIds.value = []
    selectedChosenIds.value = []
}

const completeList = ref([]) // 설정완료 된 타겟팅 list

// 타겟팅 조건 설정 완료 버튼 클릭
/** 조건 선택 확정: 임시 조건을 완료 리스트로 이동 */
function selectedField(item, index) {
    const key = item.key
    const extra = extraValues[key] || {}

    if (!extra.inputValue || extra.inputValue.trim() === '') {
        showAlert(
            TARGET_TYPE_VIEW_MAP.find((t) => t.value === 'inputGuideEmptyValue')
                ?.label,
            '',
            'error'
        )
        return
    }

    // ✅ 최신 extraValues 반영 후 push (영구 그룹 id 부여)
    const newNode = reactive({
        ...item,
        extraValues: extra,
        depth: 0,
        _isEditing: item._isEditing ?? false
    })
    completeList.value.push(newNode)
    targetConditionList.value.splice(index, 1)
    if (DEBUG_TOGGLE) console.debug('completeList', completeList.value)
}

/** 조건 편집 시작: 현재 값 백업 후 편집 모드 전환 */
// 편집 상태를 원본 노드(completeList) 기준으로 유지하기 위한 헬퍼
function resolveSourceNode(node) {
    // 견고성: __completeIndex 가정(최상위 인덱스 아님)을 무시하고,
    // 먼저 참조 비교로 찾고, 없으면 키로 completeList를 재귀 탐색
    try {
        if (!node) return null
        const targetKey = node.key

        function findRec(list) {
            if (!Array.isArray(list)) return null
            for (const item of list) {
                if (item === node) return item
                if (targetKey && item?.key === targetKey) return item
                if (Array.isArray(item?.group)) {
                    const found = findRec(item.group)
                    if (found) return found
                }
            }
            return null
        }

        return findRec(completeList.value) || node
    } catch (e) {
        console.warn('[resolveSourceNode] failed:', e)
        return node
    }
}

function startEdit(node) {
    const src = resolveSourceNode(node)
    if (!src) return
    // extraValues 존재 보장(전역 extraValues 맵과 연결)
    if (!src.extraValues) {
        const defaults = {
            inputType: '1',
            inputTypeLabel: '직접입력',
            operator: 'A1',
            operatorLabel: '동등 (=)',
            inputValue: ''
        }
        const key = src.key
        if (key) {
            extraValues[key] = extraValues[key] || { ...defaults }
            src.extraValues = extraValues[key]
        } else {
            src.extraValues = { ...defaults }
        }
    }
    try {
        src._backup = JSON.parse(JSON.stringify(src.extraValues))
    } catch (e) {
        // stringify가 undefined를 반환하거나 실패한 경우 대체
        src._backup = { ...(src.extraValues || {}) }
    }
    src._isEditing = true
}

/** 조건 편집 적용: 편집 모드 종료 */
function applyEdit(node) {
    const src = resolveSourceNode(node)
    src._isEditing = false
    src._backup = null
}

/** 조건 편집 취소: 백업 값으로 롤백 */
function cancelEdit(node) {
    const src = resolveSourceNode(node)
    if (src._backup) {
        // 객체 교체 대신 덮어쓰기
        const backup = src._backup
        Object.keys(src.extraValues || {}).forEach(
            (k) => delete src.extraValues[k]
        )
        Object.assign(src.extraValues, backup)
    }
    src._isEditing = false
    src._backup = null
}

/** 전체 초기화: 조건/완료 리스트 및 추가값 리셋 */
function resetTargetingList() {
    const hasWork =
        (Array.isArray(targetConditionList.value) &&
            targetConditionList.value.length > 0) ||
        (Array.isArray(completeList.value) && completeList.value.length > 0) ||
        Object.keys(extraValues || {}).length > 0

    if (!hasWork) {
        // 진행중 작업이 없을 때는 경고창 대신 안내만 노출하거나 조용히 종료
        showAlert('초기화할 항목이 없습니다.', '', 'info')
        return
    }

    showConfirm(
        '진행중인 작업이 존재 합니다. \n초기화 하시겠습니까?',
        '',
        { icon: 'warning' },
        async () => {
            targetConditionList.value = []
            completeList.value = []
            Object.keys(extraValues).forEach((key) => {
                delete extraValues[key]
            })
        }
    )
}

/** 노드 삭제: 플랫 노드 기준으로 원본 트리에서 제거하고 그룹/커넥터 정리 */
function deleteNode(node) {
    __printStructure(`BEFORE deleteNode key=${node?.key}`)
    const target = resolveSourceNode(node)
    if (!target) return

    // parent 컨테이너와 인덱스 찾기
    function findParentContainer(targetNode, list = completeList.value) {
        for (let i = 0; i < list.length; i++) {
            const item = list[i]
            if (item === targetNode) return { parent: list, index: i }
            if (Array.isArray(item?.group)) {
                const childList = item.group
                for (let j = 0; j < childList.length; j++) {
                    if (childList[j] === targetNode) {
                        return { parent: childList, index: j }
                    }
                }
                const deeper = findParentContainer(targetNode, childList)
                if (deeper) return deeper
            }
        }
        return null
    }

    // 특정 children 리스트를 보유한 그룹 노드 찾기
    function findGroupNodeForChildren(childrenList, list = completeList.value) {
        for (const item of list) {
            if (Array.isArray(item?.group)) {
                if (item.group === childrenList) return item
                const found = findGroupNodeForChildren(item.group, item.group)
                if (found) return found
            }
        }
        return null
    }

    // 부모 ops에서 제거 후 커넥터 재배열
    function reconcileOpsOnRemoval(
        groupNode,
        removedChildIndex,
        priorChildrenLen
    ) {
        if (!groupNode || !Array.isArray(groupNode.ops)) return
        const oldOps = [...groupNode.ops]
        const m = oldOps.length // == priorChildrenLen - 1
        const k = removedChildIndex
        let newOps = []
        if (priorChildrenLen <= 1) {
            newOps = []
        } else if (k === 0) {
            // 맨 앞 원소 제거 → 첫 커넥터 제거
            newOps = oldOps.slice(1)
        } else if (k === priorChildrenLen - 1) {
            // 맨 끝 원소 제거 → 마지막 커넥터 제거
            newOps = oldOps.slice(0, m - 1)
        } else {
            // 가운데 원소 제거 → 좌/우 커넥터를 하나로 병합 (우선 next-op)
            const rightOp = oldOps[k]
            const leftOp = oldOps[k - 1]
            const contextOp =
                rightOp !== undefined
                    ? rightOp
                    : leftOp !== undefined
                    ? leftOp
                    : 'AND'
            newOps = [
                ...oldOps.slice(0, k - 1),
                contextOp,
                ...oldOps.slice(k + 1)
            ]
        }
        groupNode.ops = newOps
    }

    const where = findParentContainer(target)
    if (!where) return

    const parentList = where.parent
    const removedIdx = where.index

    // 부모가 그룹인지 확인
    const owningGroup = findGroupNodeForChildren(parentList)
    const priorChildrenLen = Array.isArray(parentList) ? parentList.length : 0

    // 실제 삭제
    parentList.splice(removedIdx, 1)

    // extraValues 정리
    try {
        if (target?.key && extraValues[target.key]) {
            delete extraValues[target.key]
        }
    } catch (e) {}

    // 그룹 내부였다면 ops 재배열
    if (owningGroup) {
        reconcileOpsOnRemoval(owningGroup, removedIdx, priorChildrenLen)
        // 자식 수에 따른 그룹 정리: 0 → 그룹 삭제, 1 → 래퍼 해제
        if (Array.isArray(owningGroup.group)) {
            if (owningGroup.group.length === 0) {
                // 그룹 자체 제거
                const whereGroup = findParentContainer(owningGroup)
                if (whereGroup) {
                    const parentOfGroup = findGroupNodeForChildren(
                        whereGroup.parent
                    )
                    const priorLen = whereGroup.parent.length
                    // 부모 ops도 재배열 필요 (그룹 항목 제거)
                    if (parentOfGroup) {
                        reconcileOpsOnRemoval(
                            parentOfGroup,
                            whereGroup.index,
                            priorLen
                        )
                    }
                    whereGroup.parent.splice(whereGroup.index, 1)
                }
            } else if (owningGroup.group.length === 1) {
                // 래퍼 해제: 자식으로 치환
                const onlyChild = owningGroup.group[0]
                const whereGroup = findParentContainer(owningGroup)
                if (whereGroup) {
                    whereGroup.parent.splice(whereGroup.index, 1, onlyChild)
                }
            }
        }
    }

    // 재귀적으로 single-child 그룹 정리
    function collapseGroupsKeepingOrder(list) {
        const result = []
        for (const item of list) {
            if (Array.isArray(item?.group)) {
                item.group = collapseGroupsKeepingOrder(item.group)
                if (item.group.length === 1) {
                    result.push(item.group[0])
                } else if (item.group.length === 0) {
                    // drop empty group
                } else {
                    result.push(item)
                }
            } else {
                result.push(item)
            }
        }
        return result
    }

    completeList.value = collapseGroupsKeepingOrder(completeList.value)
    // 반응성 트리거
    completeList.value = [...completeList.value]

    __printStructure(`AFTER deleteNode key=${node?.key}`)
}

/** 이동 가능 여부: 같은 부모 컨테이너 내에서 이전/다음 리프 존재 여부 판단 */
function canMoveUp(flatIdx) {
    const leaf = flattenedList.value[flatIdx]
    if (!leaf) return false
    const target = resolveSourceNode(leaf)
    if (!target) return false

    function findParentContainer(targetNode, list = completeList.value) {
        for (let i = 0; i < list.length; i++) {
            const item = list[i]
            if (item === targetNode) return { parent: list, index: i }
            if (Array.isArray(item?.group)) {
                const childList = item.group
                for (let j = 0; j < childList.length; j++) {
                    if (childList[j] === targetNode) {
                        return { parent: childList, index: j }
                    }
                }
                const deeper = findParentContainer(targetNode, childList)
                if (deeper) return deeper
            }
        }
        return null
    }

    const where = findParentContainer(target)
    if (!where) return false
    return where.index > 0
}

function canMoveDown(flatIdx) {
    const leaf = flattenedList.value[flatIdx]
    if (!leaf) return false
    const target = resolveSourceNode(leaf)
    if (!target) return false

    function findParentContainer(targetNode, list = completeList.value) {
        for (let i = 0; i < list.length; i++) {
            const item = list[i]
            if (item === targetNode) return { parent: list, index: i }
            if (Array.isArray(item?.group)) {
                const childList = item.group
                for (let j = 0; j < childList.length; j++) {
                    if (childList[j] === targetNode) {
                        return { parent: childList, index: j }
                    }
                }
                const deeper = findParentContainer(targetNode, childList)
                if (deeper) return deeper
            }
        }
        return null
    }

    const where = findParentContainer(target)
    if (!where) return false
    const parentList = where.parent
    return where.index < parentList.length - 1
}

/** 노드 위로 이동: 같은 부모 컨테이너 내에서 이전 리프와 순서 교체(리프 기준, 그룹은 건너뜀) */
function moveUp(flatIdx) {
    const leaf = flattenedList.value[flatIdx]
    if (!leaf) return
    __printStructure(`BEFORE moveUp idx=${flatIdx}`)

    const target = resolveSourceNode(leaf)
    if (!target) return

    function findParentContainer(targetNode, list = completeList.value) {
        for (let i = 0; i < list.length; i++) {
            const item = list[i]
            if (item === targetNode) return { parent: list, index: i }
            if (Array.isArray(item?.group)) {
                const childList = item.group
                for (let j = 0; j < childList.length; j++) {
                    if (childList[j] === targetNode) {
                        return { parent: childList, index: j }
                    }
                }
                const deeper = findParentContainer(targetNode, childList)
                if (deeper) return deeper
            }
        }
        return null
    }

    const where = findParentContainer(target)
    if (!where) return
    const parentList = where.parent
    const i = where.index
    if (i <= 0) return // 맨 앞이면 이동 불가

    // 이전 엔티티(그룹 포함)로 이동 허용: 단, 동일 부모 컨테이너 내에서만
    const j = i - 1
    if (j < 0) return

    // reorder: target을 꺼내 j 위치로 삽입
    const [nodeToMove] = parentList.splice(i, 1)
    parentList.splice(j, 0, nodeToMove)

    // ops는 위치 기반으로 유지 (불변)
    completeList.value = [...completeList.value]
    __printStructure(`AFTER moveUp idx=${flatIdx}`)
}

/** 노드 아래로 이동: 같은 부모 컨테이너 내에서 다음 리프와 순서 교체(리프 기준, 그룹은 건너뜀) */
function moveDown(flatIdx) {
    const leaf = flattenedList.value[flatIdx]
    if (!leaf) return
    __printStructure(`BEFORE moveDown idx=${flatIdx}`)

    const target = resolveSourceNode(leaf)
    if (!target) return

    function findParentContainer(targetNode, list = completeList.value) {
        for (let i = 0; i < list.length; i++) {
            const item = list[i]
            if (item === targetNode) return { parent: list, index: i }
            if (Array.isArray(item?.group)) {
                const childList = item.group
                for (let j = 0; j < childList.length; j++) {
                    if (childList[j] === targetNode) {
                        return { parent: childList, index: j }
                    }
                }
                const deeper = findParentContainer(targetNode, childList)
                if (deeper) return deeper
            }
        }
        return null
    }

    const where = findParentContainer(target)
    if (!where) return
    const parentList = where.parent
    const i = where.index
    if (i >= parentList.length - 1) return // 맨 끝이면 이동 불가

    // 다음 엔티티(그룹 포함)로 이동 허용: 단, 동일 부모 컨테이너 내에서만
    const j = i + 1
    if (j >= parentList.length) return

    // 재배치: i 위치 원소를 꺼내 j (리프) 뒤로 넣기
    const [nodeToMove] = parentList.splice(i, 1)
    // 주의: 원래 i<j였고 하나 제거했으니, 삽입 지점은 j-1의 다음 위치가 되어야 함
    // 하나 제거 후 index가 하나 당겨졌으므로, j-1의 다음에 삽입하는 것이 j와 동일
    parentList.splice(j, 0, nodeToMove)

    completeList.value = [...completeList.value]
    __printStructure(`AFTER moveDown idx=${flatIdx}`)
}

// 드래그 노드 출력 조건에 드랍
// ============================================================
// 섹션: 출력(보고서) 필드 드롭
// ============================================================
/** 드롭(출력): 드래그한 항목을 출력 필드 리스트에 추가 */
function onDropToTargetReportList(event) {
    let payloadNode = null
    try {
        const dt =
            event &&
            (event.dataTransfer ||
                (event.originalEvent && event.originalEvent.dataTransfer))
        if (dt) {
            const json = dt.getData && dt.getData('application/json')
            const txt = dt.getData && dt.getData('text/plain')
            if (json) {
                try {
                    payloadNode = JSON.parse(json)
                } catch (e) {
                    console.warn(
                        '[onDropToTargetReportList] failed to parse json payload:',
                        e
                    )
                }
            }
            if (!payloadNode && txt) {
                // 일반 텍스트에 key가 포함되어 있을 가능성 큼
                const key = txt
                const findNodeRec = (nodes, k) => {
                    for (const n of nodes || []) {
                        if (n.key === k) return n
                        if (n.children) {
                            const r = findNodeRec(n.children, k)
                            if (r) return r
                        }
                    }
                    return null
                }
                payloadNode = findNodeRec(metaTableList.value, key) || null
            }
        }
    } catch (e) {
        console.warn(
            '[onDropToTargetReportList] error reading dataTransfer:',
            e
        )
    }

    const sourceNode = payloadNode || draggedNode.value
    if (!sourceNode) {
        console.warn(
            '[onDropToTargetReportList] no source node available for drop'
        )
        return
    }

    const sourceKey = sourceNode?.key
    if (!sourceKey) {
        console.warn(
            '[onDropToTargetReportList] source node has no key',
            sourceNode
        )
        return
    }

    const existing = targetReportList.value.find((k) => k.key == sourceKey)
    if (existing) {
        showAlert(
            existing.metaFieldName + ' \n 항목은 이미 등록되어 있습니다.',
            '',
            'warning'
        )
        // 사용되었다면 draggedNode 참조 해제
        if (draggedNode.value && draggedNode.value === sourceNode)
            draggedNode.value = null
        return
    }

    targetReportList.value.push({ ...sourceNode })
    // draggedNode 참조 해제
    if (draggedNode.value && draggedNode.value === sourceNode)
        draggedNode.value = null
}

// ============================================================
// 섹션: 출력 함수(집계/가공) 모달
// ============================================================
const isOutputFunctionModalOpen = ref(false) // 출력함수 모달 on/off
const selectedOutputFunctionRow = ref(null) // 선택된 출력 함수
const outputFunctionParamValues = ref([]) // 선택된 출력 함수의 인수 갯수
const outputFunctionList = ref([]) // 출력함수 list
const currentChip = ref(null) // 모달 열 때 선택한 칩

// 특수(가변 페어) 함수 ID 목록: CASE와 동일하게 조건/결과 페어를 사용
const CASE_LIKE_FUNCTION_IDS = new Set(['TF0000000020'])
const isCaseLike = (fn) => {
    if (!fn) return false
    return (
        fn.targetFunctionName === 'case' ||
        CASE_LIKE_FUNCTION_IDS.has(String(fn.targetFunctionId))
    )
}

/** 출력 함수/칩 제거: 연결된 출력 필드 및 저장 데이터 동기 삭제 */
function deleteOutputFunctionRow(chip) {
    try {
        if (DEBUG_TOGGLE) console.debug('삭제(행):', chip)

        // 1) targetReportList에서 해당 칩 제거
        if (Array.isArray(targetReportList.value)) {
            targetReportList.value = targetReportList.value.filter(
                (c) => c.key !== chip.key
            )
        }

        // 2) chips 배열도 관리 중이면 동기화(옵션)
        if (Array.isArray(chips.value)) {
            chips.value = chips.value.filter((c) => c.id !== chip.id)
        }

        // 3) 해당 칩의 저장된 outputFunctionSaveData 엔트리 제거
        if (
            chip &&
            chip.key &&
            outputFunctionSaveData &&
            outputFunctionSaveData.value &&
            Object.prototype.hasOwnProperty.call(
                outputFunctionSaveData.value,
                chip.key
            )
        ) {
            const copy = { ...outputFunctionSaveData.value }
            delete copy[chip.key]
            outputFunctionSaveData.value = copy
            if (DEBUG_TOGGLE)
                console.debug(
                    '[deleteOutputFunctionRow] 저장 엔트리 제거:',
                    chip.key
                )
        }
    } catch (e) {
        console.error('[deleteOutputFunctionRow] 처리 중 오류', e)
    }
}

// 출력함수 list select & 모달 띄우기
/** 출력 함수 모달 표시: 목록 조회 및 기존 저장 파라미터 복원 */
const showOutputFunctionModal = async ({ funcName, chip }) => {
    const response = await expertModules.selectTargetFunctionList()
    console.log('출력함수', response)
    if (response) {
        outputFunctionList.value = response.targetFunctionList

        // 선호 함수 결정: ID 우선 → 이름
        const savedFn =
            chip && outputFunctionSaveData.value
                ? outputFunctionSaveData.value[chip.key]?.function
                : null
        const preferredId =
            chip?.targetFunctionId || savedFn?.targetFunctionId || null
        const preferredName =
            chip?.funcName || savedFn?.targetFunctionName || funcName || null

        let func = null
        if (preferredId != null) {
            func = outputFunctionList.value.find(
                (f) => String(f.targetFunctionId) === String(preferredId)
            )
        }
        if (!func && preferredName) {
            func = outputFunctionList.value.find(
                (f) => f.targetFunctionName === preferredName
            )
        }
        if (!func) func = outputFunctionList.value[0]

        selectedOutputFunctionRow.value = func

        // 해당 칩에 저장된 인수가 있으면 복원
        const savedEntry =
            chip && outputFunctionSaveData.value
                ? outputFunctionSaveData.value[chip.key]
                : null
        const savedParams = savedEntry ? savedEntry.params : null

        const paramCountRaw =
            func.params?.length ?? func.targetFunctionParamCnt ?? 0
        const paramCount =
            Number.isFinite(paramCountRaw) && paramCountRaw > 0
                ? Math.floor(paramCountRaw)
                : 0

        if (func.targetFunctionId === 'TF0000000020') {
            // 통합 저장 인수에서 caseParamPairs 복원
            if (Array.isArray(savedParams) && savedParams.length > 0) {
                caseParamPairs.value = savedParams.map((p) => ({
                    condition: p.condition ?? '',
                    result: p.result ?? ''
                }))
            } else {
                // 최소 1개의 빈 쌍 보장
                if (
                    !Array.isArray(caseParamPairs.value) ||
                    caseParamPairs.value.length === 0
                ) {
                    caseParamPairs.value = [{ condition: '', result: '' }]
                }
            }
            // CASE의 경우 인수1은 칩의 필드명으로 항상 보여줘야 함
            if (!Array.isArray(outputFunctionParamValues.value))
                outputFunctionParamValues.value = []
            outputFunctionParamValues.value[0] = chip ? chip.metaFieldName : ''
        } else {
            if (Array.isArray(savedParams) && savedParams.length > 0) {
                const arr = savedParams.map((p) =>
                    p && p.result != null ? p.result : ''
                )
                const trimmed = arr.slice(0, paramCount)
                while (trimmed.length < paramCount) trimmed.push('')
                // 인수1(라벨)은 항상 칩 필드명 반영
                if (paramCount > 0) trimmed[0] = chip ? chip.metaFieldName : ''
                outputFunctionParamValues.value = trimmed
            } else {
                outputFunctionParamValues.value = Array.from(
                    { length: paramCount >= 0 ? paramCount : 0 },
                    (_, i) => (i === 0 ? (chip ? chip.metaFieldName : '') : '')
                )
            }
        }

        currentChip.value = chip
        isOutputFunctionModalOpen.value = true
    }
}

// 💡 CASE 함수일 때 조건/결과 세트
const caseParamPairs = ref([
    { condition: '', result: '' } // 기본 1세트
])

// ✅ 라벨 결정 함수
/** 파라미터 라벨 반환: CASE/일반 함수 각각 대응 */
function getParamLabel(funcName, idx) {
    // 선택된 함수가 CASE 또는 CASE-유사(ID 기준)인지 판단
    const curr = selectedOutputFunctionRow.value
    const caseLike =
        curr &&
        (curr.targetFunctionName === 'case' ||
            CASE_LIKE_FUNCTION_IDS.has(String(curr.targetFunctionId)))
    if (caseLike) {
        if (idx === 1) return '조건'
        if (idx === 2) return '결과'
    }
    return `인수 ${idx + 1}`
}

// ✅ CASE용 조건/결과 세트 추가
/** CASE 조건/결과 페어 추가 */
function addCasePair() {
    if (!Array.isArray(caseParamPairs.value))
        caseParamPairs.value = [{ condition: '', result: '' }]
    else caseParamPairs.value.push({ condition: '', result: '' })
}

// 출력함수 선택
/** 출력 함수 선택: 파라미터 입력칸 갯수 및 기본값 구성 */
function selectedOutputFunction(func) {
    if (!func) return

    selectedOutputFunctionRow.value = JSON.parse(JSON.stringify(func))

    // ✅ 인수 개수만큼 배열 만들기
    const paramCountRaw =
        func.params?.length ?? func.targetFunctionParamCnt ?? 0
    const paramCount =
        Number.isFinite(paramCountRaw) && paramCountRaw > 0
            ? Math.floor(paramCountRaw)
            : 0

    // ✅ 첫 번째 인수에 chip을 넣고 나머지는 빈칸으로
    outputFunctionParamValues.value = Array.from(
        { length: paramCount >= 0 ? paramCount : 0 },
        (_, i) =>
            i === 0
                ? currentChip.value
                    ? currentChip.value.metaFieldName
                    : ''
                : ''
    )
}

// 칩별(키 기준) 저장된 출력함수 데이터
// 형태: { [chipKey]: { function, params, chip, savedAt } }
const outputFunctionSaveData = ref({})

// 출력함수 저장
/** 출력 함수 저장: 칩 key 기준으로 통합된 파라미터 구조 보관 */
function saveOutputFunction() {
    try {
        const fn = selectedOutputFunctionRow.value
            ? JSON.parse(JSON.stringify(selectedOutputFunctionRow.value))
            : null

        // 인수 형식 통일: [{condition, result}, ...] 형태로 변환
        let unifiedParams = []
        if (fn && fn.targetFunctionName === 'case') {
            unifiedParams = (caseParamPairs.value || []).map((p) => ({
                condition: p.condition ?? '',
                result: p.result ?? ''
            }))
        } else if (Array.isArray(outputFunctionParamValues.value)) {
            unifiedParams = outputFunctionParamValues.value.map((v, idx) => ({
                condition: String(idx + 1),
                result: v ?? ''
            }))
        }

        const payload = {
            function: fn,
            params: unifiedParams,
            chip: currentChip.value
                ? {
                      metaFieldId: currentChip.value.metaFieldId,
                      metaFieldName: currentChip.value.metaFieldName,
                      key: currentChip.value.key
                  }
                : null,
            savedAt: new Date().toISOString()
        }

        // 칩 키(chip.key)로 페이로드 저장
        if (payload && payload.chip && payload.chip.key) {
            outputFunctionSaveData.value = {
                ...outputFunctionSaveData.value,
                [payload.chip.key]: payload
            }
            // UI 보조: 해당 칩의 funcName도 동기화하여 버튼 active를 직관적으로 유지
            try {
                const idx = targetReportList.value.findIndex(
                    (c) => c.key === payload.chip.key
                )
                if (idx !== -1) {
                    const updated = {
                        ...targetReportList.value[idx],
                        funcName: fn?.targetFunctionName || null,
                        targetFunctionId: fn?.targetFunctionId || null
                    }
                    targetReportList.value.splice(idx, 1, updated)
                }
            } catch {}
        } else {
            console.warn('[saveFunction] 저장할 칩 키가 없습니다')
        }
    } catch (e) {
        console.error('[saveFunction] 페이로드 생성 실패', e)
        // 실패 시 전체 맵을 덮어쓰지 않도록 주의
    }
    isOutputFunctionModalOpen.value = false
}

// 안전한 인수 입력 갯수 계산: targetFunctionParamCnt - 1 (최소 0)
const outputFunctionParamInputCount = computed(() => {
    const cntRaw = selectedOutputFunctionRow.value?.targetFunctionParamCnt ?? 0
    const cnt = Number.isFinite(cntRaw) && cntRaw > 0 ? Math.floor(cntRaw) : 0
    return Math.max(0, cnt - 1)
})

// 선택된 함수가 CASE-유사(ID 포함)인지 템플릿에서 사용
const isCaseLikeSelected = computed(() =>
    isCaseLike(selectedOutputFunctionRow.value)
)

// 삭제
/** 출력 함수 삭제: 저장 데이터/입력 상태 초기화 후 모달 종료 */
function deleteOutputFunction() {
    try {
        const chip = currentChip.value

        // 만약 칩에 저장된 출력함수 데이터가 있으면 해당 엔트리를 완전히 삭제
        if (
            chip &&
            chip.key &&
            outputFunctionSaveData &&
            outputFunctionSaveData.value &&
            Object.prototype.hasOwnProperty.call(
                outputFunctionSaveData.value,
                chip.key
            )
        ) {
            const copy = { ...outputFunctionSaveData.value }
            delete copy[chip.key]
            outputFunctionSaveData.value = copy
            if (DEBUG_TOGGLE)
                console.debug(
                    '[deleteOutputFunction] 칩 저장 엔트리 제거:',
                    chip.key
                )
        } else {
            if (DEBUG_TOGGLE)
                console.debug(
                    '[deleteOutputFunction] 저장된 엔트리 없음:',
                    chip?.key ?? '(no-chip)'
                )
        }

        // UI 상태 초기화: 선택 함수, 인수(단, 인수1은 칩명으로 보존), CASE 세트 초기화
        selectedOutputFunctionRow.value = null
        if (!Array.isArray(outputFunctionParamValues.value))
            outputFunctionParamValues.value = []
        outputFunctionParamValues.value[0] = currentChip.value
            ? currentChip.value.metaFieldName
            : ''
        caseParamPairs.value = [{ condition: '', result: '' }]
        // 칩의 표시용 funcName 제거
        if (chip && chip.key) {
            const idx = targetReportList.value.findIndex(
                (c) => c.key === chip.key
            )
            if (idx !== -1) {
                const updated = { ...targetReportList.value[idx] }
                delete updated.funcName
                delete updated.targetFunctionId
                targetReportList.value.splice(idx, 1, updated)
            }
        }
    } catch (e) {
        console.error('[deleteOutputFunction] 처리 중 오류', e)
    } finally {
        // 모달 닫음
        isOutputFunctionModalOpen.value = false
    }
}
// 출력 함수 모달 닫힐때
/** CASE 파라미터 페어 초기화 및 일반 파라미터 입력 초기화 */
function resetCaseParamPairs() {
    // ✅ CASE용 데이터 초기화
    caseParamPairs.value = [{ condition: '', result: '' }]
    // ✅ 일반 인수 입력값도 초기화해두면 안전
    outputFunctionParamValues.value = []
    selectedOutputFunctionRow.value = {}
}

// 목적, 주제영역 변경시 드랍 list 초기화
function setDefault() {
    targetConditionList.value = []
    targetReportList.value = []
    completeList.value = []
}

// targetReportList 초기화 시 저장된 outputFunction 데이터도 함께 초기화
function resetTargetReportList() {
    try {
        targetReportList.value = []
        // outputFunctionSaveData는 칩 key 별 저장소이므로 전체 초기화
        outputFunctionSaveData.value = {}
        if (DEBUG_TOGGLE)
            console.debug(
                '[resetTargetReportList] targetReportList 및 outputFunctionSaveData 초기화'
            )
    } catch (e) {
        console.error('[resetTargetReportList] 초기화 중 오류', e)
    }
}

// ============================================================
// 섹션: CompleteList 내보내기(1차원 배열)
// 요구사항: 현재 completeList의 노드 데이터를 "그대로" 보존하되,
// - 화면상 depth를 포함하고(서버와 일치: conditionDepth)
// - AND/OR 버튼 상태를 각 버튼 "위" 노드에 매핑 (마지막 노드는 null, 서버와 일치: condition)
// - 결과는 1차원 배열로 반환/로그 출력
// 구현: flattenedList + buttonStates를 이용해 즉시 구성
// ============================================================
function getFlatCompleteList() {
    try {
        const flat = Array.isArray(flattenedList.value)
            ? toRaw(flattenedList.value)
            : []
        const buttonsArr = Array.isArray(buttonStates.value)
            ? toRaw(buttonStates.value)
            : []
        const connectors = Array.isArray(connectorDepths.value)
            ? toRaw(connectorDepths.value)
            : []

        // 순수 깊은 복사(순환/함수 제거)용 replacer
        const replacer = (key, value) => {
            if (key === '__nodeRef') return undefined // 순환 방지
            if (typeof value === 'function') return undefined
            return value
        }

        const exported = flat.map((n, i) => {
            const btn = i < flat.length - 1 ? buttonsArr[i] : null
            const btnOp = btn && btn.conditionType ? btn.conditionType : null
            // 노드 데이터 전체 복사 (순환키 제거)
            let clone
            try {
                clone = JSON.parse(JSON.stringify(n, replacer))
            } catch (e) {
                // fallback: 얕은 복사 + 중요한 값 보강
                clone = {
                    ...n,
                    extraValues: n?.extraValues ? { ...n.extraValues } : null
                }
                delete clone.__nodeRef
            }
            // 서버 포맷과 동일한 이름으로 내보냄
            clone.condition = btnOp
            // label 보조 필드 (가독성)
            if (!clone.label)
                clone.label = n?.metaFieldName || n?.title || n?.key
            // depth 보강 및 서버 키 동기화
            // - depth: 화면상 leaf 들여쓰기 깊이
            // - conditionDepth: 이 leaf 가 속한 그룹(버튼 스코프)의 깊이
            const leafDepth =
                typeof n.depth === 'number' ? n.depth : Number(n.depth) || 0

            let groupDepth = leafDepth
            // i번째 leaf 오른쪽 커넥터의 depth를 우선 사용
            if (i < connectors.length) {
                const connDepth = connectors[i]?.depth
                if (typeof connDepth === 'number') {
                    groupDepth = connDepth
                }
            } else if (typeof n.groupDepth === 'number') {
                // 폴백: 미리 계산된 groupDepth가 있으면 사용
                groupDepth = n.groupDepth
            }

            clone.depth = leafDepth
            clone.conditionDepth = groupDepth
            // 내부 키 정리
            delete clone.button
            return clone
        })

        // 디버그 모드에서만 전체 데이터 출력
        if (DEBUG_TOGGLE) {
            console.log('[checkCompleteList] Export (full)')
            console.log(exported)
            console.groupEnd()
        }

        return exported
    } catch (e) {
        console.error('[checkCompleteList] 실패:', e)
        return []
    }
}

// ============================================================
// 섹션: 1차원(flat) → 다차원(completeList) 복원
// 요구사항: checkCompleteList()로 저장된 1차원 배열을 다시 그룹 구조로 복원한다.
// 가정/규칙:
//  - 각 항목은 depth(정수)와 button(다음 항목과의 AND/OR)을 가진다.
//  - depth 증감은 그룹의 중첩(_indent 합)과 일치한다.
//  - 내부 그룹의 ops는 인접 자식 사이에 대응되며, i와 i+1의 연결자는 min(depth[i], depth[i+1])의 그룹에 속한다.
//  - 최상위(depth=0)는 그룹 래퍼가 없으며 ops를 저장하지 않는다(런타임에 버튼 상태로 표현).
// 결과: completeList와 extraValues를 재구성한다.
// ============================================================

/** leaf 노드 정리: 그룹 메타 제거 및 extraValues 매핑 복원 */
function __sanitizeLeafFromFlat(item) {
    const leaf = { ...item }
    // 불필요/순환/내부 메타 제거
    delete leaf.button
    delete leaf.condition
    delete leaf.__nodeRef
    delete leaf.__groupId
    delete leaf.__groupIndex
    delete leaf.__groupLastIndex
    delete leaf.__entityAt
    delete leaf.__completeIndex

    // 편집 플래그 초기화
    leaf._isEditing = false
    leaf._backup = null

    // extraValues 링크 보강 + 연산자/라벨 정규화
    const key = leaf.key
    if (key) {
        const defaults = {
            inputType: '1',
            inputTypeLabel: '직접입력',
            operator: 'A1',
            operatorLabel: '동등 (=)',
            inputValue: ''
        }
        // 기존 값 우선, 없으면 기본값
        const base =
            leaf.extraValues && typeof leaf.extraValues === 'object'
                ? { ...leaf.extraValues }
                : { ...defaults }
        const inType = String(base.inputType || '1')
        const opCode = mapServerOperatorToCode(base.operator, inType)
        const normalized = {
            ...base,
            inputType: inType,
            inputTypeLabel: findLabelFromOptions(
                TARGET_INPUT_TYPE_OPTIONS,
                inType
            ),
            operator: opCode,
            operatorLabel: getOperatorLabelByCode(opCode, inType)
        }
        // 전역 맵에 연결
        extraValues[key] = normalized
        leaf.extraValues = extraValues[key]
        // placeholder/UI를 위해 subquery 플래그 갱신
        inputTypeSelected[key] = inType === '3'
    }

    // group 속성은 없어야 leaf로 인식됨
    if (Array.isArray(leaf.group)) delete leaf.group
    if (Array.isArray(leaf.ops)) delete leaf.ops

    // depth 정규화(숫자) - 서버 키(conditionDepth) 우선, 없으면 depth
    const d = Number(
        leaf.conditionDepth !== undefined ? leaf.conditionDepth : leaf.depth
    )
    leaf.depth = Number.isFinite(d) && d >= 0 ? d : 0
    // 원본 서버 키는 내부 leaf에서는 불필요
    delete leaf.conditionDepth
    return leaf
}

/** 1차원 배열로부터 completeList 구조 생성 (반환만 함) */
function buildCompleteListFromFlat(flat) {
    // 새 알고리즘 (v2):
    // - 서버 flat[i].conditionDepth 는 i 와 i+1 사이 커넥터(연산자)의 스코프 깊이로 본다.
    // - leaf 자체의 들여쓰기(depth)는 '직전 커넥터의 깊이'를 따른다 (첫 leaf는 0).
    // - 커넥터 깊이가 증가하면(예: 0->1) 직전 leaf를 새 그룹으로 승격(래핑) 후 그 안에 다음 leaf 추가.
    // - 커넥터 깊이가 감소하면(예: 1->0) 상위로 그룹 스택을 닫는다.
    // - 동일 깊이면 같은 그룹(또는 root) 내에서 연산자를 ops 에 추가.
    if (!Array.isArray(flat) || flat.length === 0) return []

    if (DEBUG_TOGGLE) {
        console.group('[buildCompleteListFromFlat:v2] INPUT')
        flat.forEach((row, i) => {
            console.log(
                `  [${i}] field=${row.metaFieldName} condition=${row.condition} condDepth=${row.conditionDepth}`
            )
        })
        console.groupEnd()
    }

    // root 그룹을 항상 래퍼로 사용 (연산자 depth=0 저장 가능)
    const rootGroup = { group: [], ops: [], _indent: 0, depth: 0 }
    const stack = [rootGroup] // stack[stack.length-1] = 현재 커넥터 깊이 그룹
    let currentConnectorDepth = 0 // 직전 커넥터가 적용된 깊이

    // leaf 추가 헬퍼(현재 가장 깊은 그룹에 push)
    function pushLeaf(leaf) {
        stack[stack.length - 1].group.push(leaf)
    }

    // 그룹 개설: 현재 최상위의 마지막 child(직전 leaf/그룹)를 새 그룹으로 감싼다
    function openGroup(toDepth) {
        // toDepth 까지 반복적으로 상승
        for (let level = currentConnectorDepth + 1; level <= toDepth; level++) {
            const parent = stack[stack.length - 1]
            const prev = parent.group[parent.group.length - 1]
            if (!prev) break // 안전장치
            // 새 그룹 생성, prev를 첫 child로 이동
            const newGroup = {
                group: [prev],
                ops: [],
                _indent: 1,
                depth: level
            }
            parent.group[parent.group.length - 1] = newGroup
            stack.push(newGroup)
            if (DEBUG_TOGGLE) {
                console.log(
                    `[buildCompleteListFromFlat:v2] OPEN group depth=${level} (wrap prev leaf)`
                )
            }
        }
        currentConnectorDepth = toDepth
    }

    // 그룹 닫기: 목표 깊이까지 pop
    function closeGroup(targetDepth) {
        while (stack.length > 1 && currentConnectorDepth > targetDepth) {
            stack.pop()
            currentConnectorDepth--
            if (DEBUG_TOGGLE) {
                console.log(
                    `[buildCompleteListFromFlat:v2] CLOSE to depth=${currentConnectorDepth}`
                )
            }
        }
    }

    for (let i = 0; i < flat.length; i++) {
        const raw = flat[i]
        const leaf = __sanitizeLeafFromFlat(raw)
        // leaf.depth = 직전 커넥터 깊이 (i==0 이면 0)
        leaf.depth = i === 0 ? 0 : Number(flat[i - 1]?.conditionDepth) || 0
        pushLeaf(leaf)

        // i 번째 leaf 와 i+1 leaf 사이 커넥터 처리 (마지막 leaf 제외)
        if (i < flat.length - 1) {
            const connDepth = Number(raw.conditionDepth) || 0 // 이 커넥터(연산자)의 스코프 깊이
            const op = raw.condition || 'AND'

            if (connDepth > currentConnectorDepth) {
                // 상승: 새 그룹 개설 후 커넥터 ops 할당 (새 그룹이 적용된 상태에서 다음 leaf 추가되므로 OK)
                openGroup(connDepth)
            } else if (connDepth < currentConnectorDepth) {
                // 하강: 그룹 닫고 동일/낮은 깊이로 이동
                closeGroup(connDepth)
            }
            // 현재 깊이(connDepth)에 해당하는 그룹에 연산자 기록
            // depth=0 이면 rootGroup
            const target = connDepth === 0 ? rootGroup : stack[stack.length - 1]
            target.ops.push(op)
            if (DEBUG_TOGGLE) {
                console.log(
                    `[buildCompleteListFromFlat:v2] ADD OP '${op}' at depth=${connDepth}`
                )
            }
            currentConnectorDepth = connDepth
        }
    }

    // 모든 그룹 ops 정규화: length-1 맞추기
    function normalize(group) {
        const need = Math.max(0, group.group.length - 1)
        while (group.ops.length < need) group.ops.push('AND')
        if (group.ops.length > need) group.ops.length = need
        group.group.forEach((child) => {
            if (Array.isArray(child.group)) normalize(child)
        })
    }
    normalize(rootGroup)

    if (DEBUG_TOGGLE) {
        try {
            console.group('[buildCompleteListFromFlat:v2] RESULT')
            console.log('tree:', JSON.stringify(rootGroup, null, 2))
            console.groupEnd()
        } catch {}
    }
    // 최상위는 항상 래퍼 그룹 하나로 반환
    return [rootGroup]
}

const testParam = ref({
    selectTargetAreaGroupId: 'AG0000000004',
    selectTargetAreaId: 'TA0000000150',
    selectTargetId: 'TM0000006649',
    // selectTargetUserId : ,
    expertReqestType: 'load'
})

const testParam2 = ref({ targetId: 'TM0000006649' })

/** 서버 응답(selectTargetCondition) → flat 배열로 변환 */
function mapResponseToFlat(resp) {
    const conds = (resp && resp.selectTargetCondition) || []
    // conditionOrder 기준 정렬 보장
    const sorted = [...conds].sort(
        (a, b) => (a.conditionOrder || 0) - (b.conditionOrder || 0)
    )
    const now = Date.now()
    const flat = sorted.map((row, i) => {
        const key = `${row.metaFieldId || 'MF'}_${now}_${i}`
        const depth = Number(row.conditionDepth) || 0
        const inputType = String(row.inputType || '1')
        const opCode = mapServerOperatorToCode(row.operator, inputType)
        return {
            key,
            metaFieldId: row.metaFieldId,
            metaFieldName: row.metaFieldName,
            metaTableId: row.metaTableId,
            metaTableName: row.metaTableName,
            metaFieldDataType: row.metaFieldDatatype,
            metaDimensionYn: row.metaDimensionYn,
            metaBidwDimensionYn: row.bidwMetaDimensionYn,
            label: row.metaFieldName || row.metaFieldId || key,
            conditionDepth: depth,
            // 서버 포맷 준수: 각 항목 위 버튼(op)을 condition 필드로 기록
            condition: row.condition || null,
            extraValues: {
                inputType,
                inputTypeLabel: findLabelFromOptions(
                    TARGET_INPUT_TYPE_OPTIONS,
                    inputType
                ),
                operator: opCode,
                operatorLabel: getOperatorLabelByCode(opCode, inputType),
                inputValue: row.value ?? ''
            }
        }
    })
    return flat
}

async function checkCompleteListLoad() {
    try {
        const response2 = await expertModules.selectTargetInformation(
            testParam2.value
        )
        const response = await expertModules.expertMain(testParam.value)
        // 서버 응답 로그 (expertMain)
        if (DEBUG_TOGGLE) {
        }
        // 서버 응답 로그 (selectTargetInformation)
        if (DEBUG_TOGGLE) {
            console.debug(
                '[checkCompleteListLoad] selectTargetInformation:',
                response2
            )
        }

        // 1) 상단 주제영역/그룹 영역 상태도 response로 세팅
        const areaList =
            response?.targetAreaList || response?.selectTargetAreaList || []
        targetAreaList.value = Array.isArray(areaList) ? areaList : []
        const groupList = response?.selectTargetAreaGroupList || []

        // 로드 기준으로 주제/그룹을 강제 동기화
        // 우선순위: response2(실제 타겟 정보) > response(영역 목록) > 첫번째 항목
        const respAreaIdFromTarget =
            response2?.selectTarget?.[0]?.targetAreaId ||
            response2?.selectTarget?.targetAreaId
        const respAreaIdFromList = response?.selectTargetAreaId
        const fallbackAreaId = targetAreaList.value[0]?.targetAreaId || null
        const desiredAreaId =
            respAreaIdFromTarget || respAreaIdFromList || fallbackAreaId

        const areaForGroup = targetAreaList.value.find(
            (a) => a.targetAreaId === desiredAreaId
        )
        const desiredGroupId =
            areaForGroup?.targetAreaGroupId ||
            response?.selectTargetAreaGroupId ||
            testParam.value?.selectTargetAreaGroupId ||
            null

        selectedTargetGroupArea.value =
            groupList.find((g) => g.targetAreaGroupId === desiredGroupId) ||
            groupList?.[0] ||
            null

        // 주제영역 ID 세팅 (v-model 바인딩 반영)
        selectedTargetAreaId.value = desiredAreaId || null

        if (DEBUG_TOGGLE) {
            console.debug(
                '[checkCompleteListLoad] 복원된 areaId:',
                desiredAreaId
            )
            console.debug(
                '[checkCompleteListLoad] 복원된 groupId:',
                desiredGroupId
            )
            console.debug(
                '[checkCompleteListLoad] targetAreaList:',
                targetAreaList.value
            )
            console.debug(
                '[checkCompleteListLoad] selectedTargetGroupArea:',
                selectedTargetGroupArea.value
            )
            console.debug(
                '[checkCompleteListLoad] selectedTargetAreaId:',
                selectedTargetAreaId.value
            )
        }

        // 선택된 주제영역 기준 하위 정보(metaTable, 필수조건 등) 세팅
        if (selectedTargetAreaId.value) {
            await targetAreaSelected(selectedTargetAreaId.value)
        }

        // 2) 조건(WHERE) 복원: response2 → flat → 트리
        const flat = mapResponseToFlat(response2)
        if (DEBUG_TOGGLE) {
            console.debug('[checkCompleteListLoad] mapped flat:', flat)
        }
        const ok = restoreCompleteListFromFlat(flat)
        if (DEBUG_TOGGLE) {
            console.debug('[checkCompleteListLoad] restore result:', ok)
        }
        // 출력 항목 복원
        restoreTargetReportFromResponse(response2)

        // 안전한 타겟명 추출 (서버 응답 구조 변동 대비 다중 경로 체크)
        // 서버 응답 구조: selectTarget가 배열(권장) 또는 단일 객체일 수 있음
        const loadedName = Array.isArray(response2?.selectTarget)
            ? response2.selectTarget?.[0]?.targetName || null
            : response2?.selectTarget?.targetName || null

        // 로드 완료 후 상위로 최신 상태 즉시 전달
        try {
            emit('update:data', {
                ...props.data,
                targetAreaId: jsTreeModel.value.targetAreaId,
                targetAreaGroupId:
                    selectedTargetGroupArea.value?.targetAreaGroupId,
                reportCount: (targetReportList?.value || []).length,
                targetReportList: targetReportList.value,
                outputFunctionSaveData: outputFunctionSaveData.value,
                completeList: completeList.value,
                // 헤더 표시용 타겟명 유지/갱신
                targetName: loadedName || props.data?.targetName || '',
                selectTargetCondition: getFlatCompleteList()
            })
        } catch (emitErr) {
            console.error('[checkCompleteListLoad] emit 실패:', emitErr)
        }
    } catch (e) {
        console.error('[checkCompleteListLoad] 실패:', e)
    }
}

/** 1차원 배열을 받아 completeList/extraValues를 갱신 (in-place 적용) */
function restoreCompleteListFromFlat(flat) {
    try {
        // 기존 상태 초기화(필요 시)
        completeList.value = []
        // extraValues는 key 충돌을 막기 위해 일단 보존하고, 새로 로드된 키만 덮어씀
        const keep = { ...extraValues }
        Object.keys(extraValues).forEach((k) => delete extraValues[k])

        const rebuilt = buildCompleteListFromFlat(flat)
        completeList.value = rebuilt
        // 반응성 트리거
        completeList.value = [...completeList.value]

        // extraValues 병합(새로 로드된 키는 위에서 설정됨, 나머지는 보존 옵션)
        // 필요 없다면 주석 처리 가능
        Object.keys(keep).forEach((k) => {
            if (!extraValues[k]) extraValues[k] = keep[k]
        })

        // =======================
        // 서버 condition/conditionDepth 직접 복원 (임시 그룹 재계산 이전 프레임 고정)
        // flat[i].condition 은 i 와 i+1 사이 커넥터, flat[i].conditionDepth 는 그 커넥터 depth
        // 마지막 leaf 는 커넥터 없음
        const btnCount = Math.max(0, flat.length - 1)
        const importedButtonStates = []
        const importedConnectorDepths = []
        const preCalc = {}
        for (let i = 0; i < btnCount; i++) {
            const row = flat[i] || {}
            const op = row.condition || 'AND'
            const depthVal =
                typeof row.conditionDepth === 'number'
                    ? row.conditionDepth
                    : Number(row.conditionDepth) || 0
            importedButtonStates.push({ conditionType: op, _locked: false })
            importedConnectorDepths.push({
                key: `import_${i}`,
                operator: op,
                depth: depthVal,
                parentGroupId: null
            })
            preCalc[i] = { depth: depthVal }
        }
        // 초기 버튼/커넥터/미리 계산된 depth 주입
        buttonStates.value = importedButtonStates
        connectorDepths.value = importedConnectorDepths
        preCalculatedButtonDepths.value = preCalc

        // flattenedList는 watchEffect에서 재계산되므로 여기서는 건드리지 않음

        return true
    } catch (e) {
        console.error('[restoreCompleteListFromFlat] 실패:', e)
        return false
    }
}

// ============================================================
// 섹션: 출력 조건(selectTargetItem) 복원 유틸
// - targetReportList: 칩 목록 복원
// - outputFunctionSaveData: 칩별 저장된 함수/인수 복원(있을 때)
// ============================================================
function restoreTargetReportFromResponse(resp) {
    try {
        const items = (resp && resp.selectTargetItem) || []
        targetReportList.value = []

        const now = Date.now()
        items.forEach((row, i) => {
            const chipKey = `${row.metaFieldId || 'MF'}_${now}_${i}`
            const chip = {
                key: chipKey,
                metaFieldId: row.metaFieldId,
                metaFieldName: row.metaFieldName,
                metaTableId: row.metaTableId,
                metaTableName: row.metaTableName,
                title: row.metaFieldName || row.metaFieldId || chipKey,
                label: row.metaFieldName || row.metaFieldId || chipKey,
                // 복원 시 모달 버튼 active 표현을 위해 함수명도 보조로 세팅
                funcName: row.targetFunctionName || null,
                // ID 기반 자동 매칭을 위한 보조 필드
                targetFunctionId: row.targetFunctionId || null
            }
            targetReportList.value.push(chip)

            // 함수/인수 복원(가능한 범위 내)
            const fnId = row.targetFunctionId
            // targetParameterXX 형태의 모든 파라미터를 동적으로 수집
            const paramKeys = Object.keys(row)
                .filter((k) => k.toLowerCase().startsWith('targetparameter'))
                .sort()
            const params = paramKeys
                .map((k) => row[k])
                .filter((v) => v !== undefined && v !== null)

            if (fnId) {
                // 특수 ID(TF0000000020): 서버 저장 시 조건/결과를 각각 콤마로 합쳐 저장 → 로드시 분해
                let unifiedParams = []
                if (String(fnId) === 'TF0000000020') {
                    const condStr = row.targetParameter02 || ''
                    const resStr = row.targetParameter03 || ''
                    const conds = String(condStr).split(',')
                    const ress = String(resStr).split(',')
                    const n = Math.max(conds.length, ress.length)
                    for (let k = 0; k < n; k++) {
                        unifiedParams.push({
                            condition: (conds[k] ?? '').trim(),
                            result: (ress[k] ?? '').trim()
                        })
                    }
                    // 최소 1세트 보장
                    if (unifiedParams.length === 0)
                        unifiedParams = [{ condition: '', result: '' }]
                } else {
                    unifiedParams = params.map((v, idx) => ({
                        condition: String(idx + 1),
                        result: String(v)
                    }))
                }

                const payload = {
                    function: {
                        targetFunctionId: fnId,
                        targetFunctionName:
                            row.targetFunctionName || String(fnId) // 이름 정보를 모르면 id를 대입
                    },
                    params: unifiedParams,
                    chip: {
                        metaFieldId: chip.metaFieldId,
                        metaFieldName: chip.metaFieldName,
                        key: chip.key
                    },
                    savedAt: new Date().toISOString()
                }
                outputFunctionSaveData.value = {
                    ...outputFunctionSaveData.value,
                    [chip.key]: payload
                }
            }
        })
    } catch (e) {
        console.error('[restoreTargetReportFromResponse] 실패:', e)
    }
}

// ============================================================
// 섹션: 트리 검색/확장/필터링
// ============================================================
const checkedField = ref(false) // ✅ 관점값 확장 검색
const checkedFieldFlag = ref(false) // ✅ 완전 일치
const apiKeys = ref([]) // ✅ API 응답 키 목록
const treeSearchText = ref('') // 입력 중인 검색어
const appliedSearch = ref('') // 실제 검색어 (엔터 or 클릭 시 적용)
const loading = ref(false)

const jsTreeSearchModel = ref({
    targetAreaId: '',
    empNo: '',
    searchWord: '',
    searchFlag: '',
    metaFieldId: '',
    metaFieldName: ''
})
// ✅ 검색 실행
/** 트리 검색 실행: 체크 옵션에 따라 API 키/타이틀 검색 병행 */
const onTreeSearch = async () => {
    appliedSearch.value = treeSearchText.value.trim()

    // 체크박스 OFF → 로컬 필터
    if (checkedField.value) {
        // 체크박스 ON → API 호출
        try {
            console.log('dhd?')
            loading.value = true
            const checkedFlag = checkedFieldFlag.value ? 'Y' : 'N'
            jsTreeSearchModel.value.targetAreaId =
                selectedTargetAreaId.value || ''
            jsTreeSearchModel.value.empNo = ''
            jsTreeSearchModel.value.searchWord = appliedSearch.value
            jsTreeSearchModel.value.searchFlag = checkedFlag

            // 서버에서 key 리스트만 받아옴 (await로 처리)
            const response = await expertModules.selectTreeChildKeyList(
                jsTreeSearchModel.value
            )
            // 안전하게 응답 검증 후 할당
            if (response && response.selectTreeChildKeyList.length > 0) {
                apiKeys.value = response.selectTreeChildKeyList
            } else {
                // 테스트 데이터 (개발용 하드코딩 유지)
                apiKeys.value = [
                    {
                        metaFieldId: 'MF0000000077',
                        metaFieldName: '약정여부',
                        targetAreaId: 'TA0000000427'
                    },
                    {
                        metaFieldId: 'MF0000000107',
                        metaFieldName: '단말기모델명',
                        targetAreaId: 'TA0000000427'
                    }
                ]
            }
        } catch (err) {
            console.error('❌ API 오류:', err)
            apiKeys.value = []
        } finally {
            loading.value = false
        }
    } else {
        apiKeys.value = []
    }
    // ✅ 2️⃣ 검색 후 트리 다시 펼치기
    const keys = []
    const collectKeys = (nodes) => {
        nodes.forEach((node) => {
            keys.push(node.key)
            if (node.children) collectKeys(node.children)
        })
    }
    collectKeys(metaTableList.value)
    expandedKeys.value = keys
}

// ✅ 체크박스 상태 변경 시 검색 초기화
watch(checkedField, (val) => {
    if (!val) checkedFieldFlag.value = false
    appliedSearch.value = ''
    treeSearchText.value = ''
    apiKeys.value = []
})

// ✅ 표시할 리스트 계산
/** 화면에 표시할 트리 데이터(검색/필터 반영) */
const displayList = computed(() => {
    // 기본 방어
    if (!Array.isArray(metaTableList.value)) return []

    const query = appliedSearch.value

    // 체크박스 OFF → title 검색
    if (!checkedField.value) {
        if (!query) return metaTableList.value
        const result = filterByTitle(metaTableList.value, query)
        return result.length ? result : metaTableList.value
    }

    // 체크박스 ON → API key 기반 검색
    if (!Array.isArray(apiKeys.value) || apiKeys.value.length === 0) {
        return metaTableList.value
    }

    const result = filterByKeys(metaTableList.value, apiKeys.value)
    return result.length ? result : metaTableList.value
})

/** 🔍 제목 기반 필터 */
/** 타이틀 키워드 기반 필터링 */
const filterByTitle = (nodes, keyword) => {
    const matchNode = (node) =>
        node.title.toLowerCase().includes(keyword.toLowerCase()) ||
        (node.children && node.children.some(matchNode))

    return nodes.filter(matchNode).map((node) => ({
        ...node,
        children: node.children ? filterByTitle(node.children, keyword) : []
    }))
}

/** 🔑 key 기반 필터 (API 응답 [{ parentKeys, childKeys }] 형태 대응) */
/** API로 전달받은 key 기반 필터링 (parentKeys/childKeys) */
const filterByKeys = (nodes, apiList) => {
    // parentKeys / childKeys 추출
    const parentKeySet = new Set(apiList.map((d) => d.targetAreaId))
    const childKeySet = new Set(apiList.map((d) => d.metaFieldId))

    const traverse = (list, depth = 1) =>
        list
            .filter((node) => {
                if (depth === 1 && parentKeySet.has(node.key)) {
                    return true
                } // 1dept 매칭
                if (depth === 2 && childKeySet.has(node.key)) return true // 2dept 매칭

                // 자식 중 하나라도 매칭되면 부모 유지
                return (
                    node.children &&
                    node.children.some((child) => {
                        return (
                            parentKeySet.has(child.key) ||
                            childKeySet.has(child.key) ||
                            (child.children &&
                                child.children.some((g) =>
                                    childKeySet.has(g.key)
                                ))
                        )
                    })
                )
            })
            .map((node) => ({
                ...node,
                children: node.children
                    ? traverse(node.children, depth + 1)
                    : []
            }))

    return traverse(nodes)
}

// 트리 확장 상태 보관
const expandedKeys = ref([]) // 트리 펼침 상태

/** 트리 전체 확장 */
const treeExpandAll = () => {
    const keys = []
    const collectKeys = (nodes) => {
        nodes.forEach((node) => {
            keys.push(node.key)
            if (node.children) collectKeys(node.children)
        })
    }
    collectKeys(metaTableList.value)
    expandedKeys.value = keys
}
/** 트리 전체 접기 */
const treeCollapseAll = () => {
    expandedKeys.value = []
}

//
// 4️⃣ 라이프사이클
//
// ============================================================
// 섹션: 라이프사이클
// ============================================================
onMounted(() => {
    targetingConditionCheckeds.value = targetAutoConditionList.value.map(
        (t) => t.targetId
    )
    //isCustomDropdown()
    // mainData()
})

// 컴포넌트 언마운트 시 전체 상태 초기화
onBeforeUnmount(() => {
    // 주제영역/그룹 초기화
    selectedTargetGroupArea.value = null
    selectedTargetAreaId.value = null
    targetAreaGroup.value = []
    targetAreaList.value = []

    // 조건 빌더 초기화
    completeList.value = []
    flattenedList.value = []
    buttonStates.value = []
    connectorDepths.value = []

    // 출력 항목 초기화
    targetReportList.value = []
    outputFunctionSaveData.value = {}

    // 메타테이블 초기화
    metaTableList.value = []
    jsTreeModel.value = {
        targetAreaId: '',
        originalTreeData: [],
        treeData: []
    }

    // 필수조건 초기화
    targetAutoConditionList.value = []
    targetingConditionCheckeds.value = []

    // 페이징 초기화
    Object.keys(pagingState).forEach((key) => delete pagingState[key])

    // store 초기화
    store.setTargetGroupId(null)

    if (DEBUG_TOGGLE) {
        console.log(
            '[ExpertQueryMain] 컴포넌트 언마운트: 전체 상태 초기화 완료'
        )
    }
})

// 전달 요소 정의 20251015 by hj START -->
// v-model:data 지원
// ============================================================
// 섹션: v-model(data) 연동 및 emit
// ============================================================
const props = defineProps({
    data: {
        type: Object,
        default: () => ({
            targetAreaGroupId: '',
            reportCount: 0,
            targetReportList: [],
            targetConditionList: [],
            completeList: []
        })
    },
    emitTrigger: {
        type: Number,
        default: 0
    }
})

/**
 * v-model(data) 사용처로 빌더 상태 전달
 * - trigger 값 변화에 따라 최신 상태 emit
 */
const emit = defineEmits(['update:data'])

// completeList는 트리거를 통해 requestPreviewData 호출 시에만 emit
// ------------------------------------------------------------
// 연결 조건(AND/OR) 버튼 상태 관리
// ------------------------------------------------------------
// 미리보기 요청 트리거 시점에 최신 데이터 emit
watch(
    () => props.emitTrigger,
    (newValue) => {
        if (newValue > 0) {
            emit('update:data', {
                ...props.data,
                targetAreaId: jsTreeModel.value.targetAreaId,
                targetAreaGroupId:
                    selectedTargetGroupArea.value.targetAreaGroupId,
                reportCount: (targetReportList?.value || []).length,
                targetReportList: targetReportList.value,
                completeList: completeList.value,
                // 저장용 1차원 조건 배열 (conditionDepth/condition 포함)
                selectTargetCondition: getFlatCompleteList(),
                // 헤더 표시용 타겟명 유지 (로드 이후 값이 있으면 그대로 전달)
                targetName: props.data?.targetName || '',
                outputFunctionSaveData: outputFunctionSaveData.value
            })
        }
    }
)
// --> 전달 요소 정의 20251015 by hj END
// --------------------
// 마지막 노드 숨김
// --------------------

/** ✅ AND/OR 상태 배열 (노드 사이의 버튼 상태) */
const buttonStates = ref([])
/** ✅ 버튼 인덱스-키 매핑: finalConnectorList 순서의 key 배열 */
const buttonIndexKeyMap = ref([])
// ✅ 렌더링 직전에 커넥터 목록(연산자 포함)을 직접 참조하기 위한 캐시
const renderConnectorList = ref([])

/** ✅ 버튼 라벨 getter (depth 포함) */
function getConditionLabel(idx) {
    // 1) 최우선: 최종 커넥터 리스트에 저장된 operator
    const conn = renderConnectorList.value[idx - 1]
    if (conn && conn.operator) return conn.operator
    // 2) 보조: 기존 buttonStates 매핑
    const fallback = buttonStates.value[idx - 1]?.conditionType
    return fallback || 'AND'
}

const flattenedList = ref([]) // UI에 렌더링되는 평면 리스트
const groupEntryButtons = ref(new Set()) // class 붙일 버튼 idx 저장

/** ✅ 헬퍼: completeList에서 노드를 찾고 작업 */
function findNodesInCompleteList(predicate, action) {
    let found = false

    function traverse(node) {
        if (found) return

        if (Array.isArray(node.group)) {
            for (let i = 0; i < node.group.length - 1; i++) {
                if (predicate(node.group, i)) {
                    action(node.group, i)
                    found = true
                    return
                }
            }
            node.group.forEach((child) => traverse(child))
        }
    }

    // completeList 최상위에서 먼저 (인접 쌍만 체크)
    for (let i = 0; i < completeList.value.length - 1; i++) {
        if (predicate(completeList.value, i)) {
            action(completeList.value, i)
            return true
        }
    }

    // 내부에서 탐색
    completeList.value.forEach((root) => traverse(root))
    return found
}

/** ✅ 그룹 병합 */
// 디버그: 전체 리스트/커넥터/플랫 배열 스냅샷 출력
function __printStructure(tag = '') {
    if (!DEBUG_TOGGLE) return
    const rawList = toRaw(completeList.value)
    const rawConnectors = toRaw(connectorDepths.value)
    const rawButtons = toRaw(buttonStates.value)
    const rawFlat = toRaw(flattenedList.value)

    function toPureNode(item) {
        if (Array.isArray(item?.group)) {
            return {
                type: 'G',
                depth: item.depth ?? 0,
                _indent: item._indent || 0,
                ops: Array.isArray(item.ops) ? [...item.ops] : [],
                size: Array.isArray(item.group) ? item.group.length : 0,
                children: item.group.map(toPureNode)
            }
        }
        return {
            type: 'L',
            depth: item?.depth ?? 0,
            key: item?.key,
            label: item?.metaFieldName || item?.title || item?.key
        }
    }

    // 텍스트 트리(간단 확인)
    function printTree(list, indent = '') {
        for (let i = 0; i < list.length; i++) {
            const item = list[i]
            if (Array.isArray(item?.group)) {
                const ops = Array.isArray(item.ops) ? item.ops.join(',') : ''
                console.log(
                    `${indent}[${i}] G depth=${item.depth ?? 0} _indent=${
                        item._indent || 0
                    } size=${
                        Array.isArray(item.group) ? item.group.length : 0
                    } ops=[${ops}]`
                )
                printTree(item.group, indent + '  ')
            } else {
                const label =
                    item?.metaFieldName || item?.title || item?.key || ''
                console.log(
                    `${indent}[${i}] L depth=${item?.depth ?? 0} key=${
                        item?.key || ''
                    } label=${label}`
                )
            }
        }
    }

    const snapshot = {
        list: Array.isArray(rawList) ? rawList.map(toPureNode) : [],
        buttons: Array.isArray(rawButtons)
            ? rawButtons.map((b, i) => ({
                  i,
                  op: b?.conditionType,
                  lock: b?._locked
              }))
            : [],
        connectors: Array.isArray(rawConnectors)
            ? rawConnectors.map((c, i) => ({
                  i,
                  op: c?.operator,
                  depth: c?.depth,
                  scope: c?.parentGroupId || 'top',
                  intra: c?._intraGroupIndex
              }))
            : [],
        flattened: Array.isArray(rawFlat)
            ? rawFlat.map((n, i) => ({
                  i,
                  depth: n?.depth ?? 0,
                  gid: n?.__groupId,
                  key: n?.key,
                  label: n?.metaFieldName || n?.title || n?.key
              }))
            : []
    }

    if (!DEBUG_TOGGLE) return
    console.group(`STRUCT ${tag}`)
    console.debug('completeList (text):')
    printTree(rawList, '')
    // 간단 수치 요약
    try {
        const topCount = Array.isArray(rawList) ? rawList.length : 0
        const flatCount = Array.isArray(rawFlat) ? rawFlat.length : 0
        console.debug(
            `SUMMARY: top-level=${topCount}, flattened=${flatCount}, buttons=${snapshot.buttons.length}, connectors=${snapshot.connectors.length}`
        )
        if (Array.isArray(rawFlat)) {
            console.debug(
                'FLAT ORDER:',
                rawFlat.map(
                    (n, i) => `${i}:${n?.key || '?'}(d${n?.depth ?? 0})`
                )
            )
        }
    } catch (e) {}
    console.debug('SNAPSHOT (pure objects):', snapshot)
    console.groupEnd()
}

function toggleCondition(idx) {
    __printStructure(`BEFORE toggleCondition idx=${idx}`)
    if (DEBUG_TOGGLE)
        console.debug(
            `\n========== toggleCondition START (idx=${idx}) ==========`
        )
    const state = buttonStates.value[idx - 1]
    if (!state) {
        if (DEBUG_TOGGLE) console.debug(`❌ state 없음`)
        return
    }

    let topNode = flattenedList.value[idx - 1]
    let bottomNode = flattenedList.value[idx]

    if (!topNode || !bottomNode) {
        if (DEBUG_TOGGLE) console.debug(`❌ topNode 또는 bottomNode 없음`)
        return
    }

    if (DEBUG_TOGGLE)
        console.log(
            `✅ topNode.depth=${topNode.depth}, bottomNode.depth=${bottomNode.depth}`
        )

    // 참고: 기존엔 depth 불일치 시 조기 반환했으나,
    // 버튼 스코프(커넥터 depth) 기준으로 그룹화가 가능해야 하므로 더 이상 막지 않음.
    const topDepth = topNode.depth ?? 0
    const bottomDepth = bottomNode.depth ?? 0
    if (topDepth !== bottomDepth && DEBUG_TOGGLE) {
        console.log(
            `⚠️ leaf depth 불일치(top=${topDepth}, bottom=${bottomDepth}) - 스코프 기준으로 진행`
        )
    }

    // 단계 1: 각 노드의 직접 부모 찾기
    function findDirectParent(node) {
        const topLevelIdx = completeList.value.indexOf(node)
        if (topLevelIdx !== -1) {
            return completeList.value
        }

        function searchInGroups(groups) {
            for (let i = 0; i < groups.length; i++) {
                const item = groups[i]
                if (Array.isArray(item.group)) {
                    for (let j = 0; j < item.group.length; j++) {
                        if (item.group[j] === node) {
                            return item.group
                        }
                    }
                    const found = searchInGroups(item.group)
                    if (found) return found
                }
            }
            return null
        }

        return searchInGroups(completeList.value)
    }

    const topParent = findDirectParent(topNode)
    const bottomParent = findDirectParent(bottomNode)
    if (DEBUG_TOGGLE)
        console.log(`📍 부모 체크: same=${topParent === bottomParent}`)

    // ⭐ 단계 2: 같은 부모에 속하면 토글만!
    // 부모가 같더라도, "형제가 있으면 그룹 생성" 규칙이 우선이므로 바로 형제 확인으로 진행
    if (DEBUG_TOGGLE) console.debug(`🔍 형제 확인 시작`)

    // 단계 3: 버튼 스코프(동일 depth 및 같은 그룹 범위)에서 동료 커넥터 존재 여부 확인
    const btnDepth = connectorDepths.value[idx - 1]?.depth ?? 0
    const currConn = connectorDepths.value[idx - 1]
    const scopeGroupId = currConn?.parentGroupId || null
    const hasPeerAtSameScope = connectorDepths.value.some((c, j) => {
        if (j === idx - 1) return false
        const sameDepth = (c?.depth ?? -1) === btnDepth
        const sameScope = scopeGroupId
            ? c?.parentGroupId === scopeGroupId
            : !c?.parentGroupId
        return sameDepth && sameScope
    })
    if (DEBUG_TOGGLE)
        console.log(
            `🔎 동일 depth 동료 존재 여부(depth=${btnDepth}, scope=${
                scopeGroupId || 'top'
            }): ${hasPeerAtSameScope}`
        )

    // 예외 규칙(보강): 최상위 스코프에서 두 엔티티(리프/그룹 무관)가 실제 top-level 컨테이너에서 인접하면
    // 동료 없어도 depth 증가 허용
    const isTopLevelScope = !scopeGroupId
    let allowByTopLevelAdjacency = false
    if (isTopLevelScope) {
        function containsEntity(entity, leaf) {
            if (entity === leaf) return true
            if (Array.isArray(entity?.group)) {
                for (const ch of entity.group) {
                    if (containsEntity(ch, leaf)) return true
                }
            }
            return false
        }
        const container = completeList.value
        for (let i = 0; i < container.length - 1; i++) {
            const leftE = container[i]
            const rightE = container[i + 1]
            const leftMatch =
                containsEntity(leftE, topNode) &&
                containsEntity(rightE, bottomNode)
            const rightMatch =
                containsEntity(leftE, bottomNode) &&
                containsEntity(rightE, topNode)
            if (leftMatch || rightMatch) {
                allowByTopLevelAdjacency = true
                break
            }
        }
    }
    if (DEBUG_TOGGLE)
        console.log(
            `🔎 최상위 예외 체크: isTopLevel=${isTopLevelScope}, top-level adjacency=${allowByTopLevelAdjacency}`
        )

    // ⭐ 항상 먼저 토글: AND -> OR, OR -> AND
    const toggledOp = state.conditionType === 'AND' ? 'OR' : 'AND'
    state.conditionType = toggledOp
    // 버튼 반응성 강제 업데이트
    buttonStates.value = [...buttonStates.value]
    if (DEBUG_TOGGLE) console.debug(`🔄 버튼 토글 결과: ${toggledOp}`)

    // ⭐ 단계 4: 동료 커넥터가 없으면 (혹은 최상위 인접 예외가 아니면)
    // - 그룹 내부 커넥터였다면 해당 그룹의 ops를 직접 토글해줘야 UI가 반영됨
    if (!hasPeerAtSameScope && !allowByTopLevelAdjacency) {
        if (DEBUG_TOGGLE)
            console.log(
                `⏭️ 동료 없음/예외 불가 → 단순 토글 (그룹 내부일 경우 ops 반영)`
            )

        // 그룹 내부 커넥터 토글 처리
        const currConn = connectorDepths.value[idx - 1]
        const scopeGroupId = currConn?.parentGroupId || null
        const intra = currConn?._intraGroupIndex
        if (scopeGroupId && typeof intra === 'number') {
            function findGroupById(groupId, list = completeList.value) {
                for (const item of list) {
                    if (Array.isArray(item?.group)) {
                        if (item.__groupId === groupId) return item
                        const found = findGroupById(groupId, item.group)
                        if (found) return found
                    }
                }
                return null
            }
            const owner = findGroupById(scopeGroupId)
            if (owner) {
                if (!Array.isArray(owner.ops)) owner.ops = []
                // 필요 길이 확보
                const need = Math.max(0, (owner.group?.length || 0) - 1)
                while (owner.ops.length < need) owner.ops.push('AND')
                if (owner.ops.length > need) owner.ops.splice(need)
                // 해당 내부 커넥터 토글 적용
                owner.ops[intra] = toggledOp
                // 반응성 트리거
                completeList.value = [...completeList.value]
            }
        }
        return
    }

    if (DEBUG_TOGGLE)
        console.log(
            `📦 그룹 생성 시작 (${
                hasPeerAtSameScope ? '스코프 OK' : '최상위 예외 적용'
            })`
        )

    // ⭐ 단계 5: 둘 다 형제가 있으면 새 그룹 생성 (시각적 들여쓰기는 _indent로만 관리)
    let newGroup = reactive({
        group: [topNode, bottomNode],
        ops: [state.conditionType],
        depth: 0,
        _indent: 1 // ✅ 새 그룹은 연산자와 무관하게 시각적 들여쓰기 +1
    })
    if (DEBUG_TOGGLE) console.debug(`✨ 새 그룹 생성: depth=${newGroup.depth}`)

    let replaced = false

    // 최상위 또는 그룹 내에서 인접 "엔티티" 찾기 (leaf 포함 여부로 판별)
    function containsNode(entity, needle) {
        if (entity === needle) return true
        if (Array.isArray(entity?.group)) {
            for (const child of entity.group) {
                if (containsNode(child, needle)) return true
            }
        }
        return false
    }

    let replacedContainer = null
    let replacedIndex = -1

    function mergeIfAdjacent(container) {
        if (!Array.isArray(container)) return false

        for (let i = 0; i < container.length - 1; i++) {
            const curr = container[i]
            const next = container[i + 1]

            const leftMatch =
                containsNode(curr, topNode) && containsNode(next, bottomNode)
            const rightMatch =
                containsNode(curr, bottomNode) && containsNode(next, topNode)
            if (leftMatch || rightMatch) {
                if (DEBUG_TOGGLE)
                    console.log(`🎯 mergeIfAdjacent 성공 at index ${i}`)
                newGroup.group = [curr, next] // 엔티티 병합
                container.splice(i, 2, newGroup)
                replacedContainer = container
                replacedIndex = i
                return true
            }
        }

        for (let i = 0; i < container.length; i++) {
            if (Array.isArray(container[i].group)) {
                if (mergeIfAdjacent(container[i].group)) {
                    return true
                }
            }
        }

        return false
    }

    if (mergeIfAdjacent(completeList.value)) {
        replaced = true
    }

    // 단계 6: 인접하지 않으면 최상위 아이템 기준으로 병합
    if (!replaced) {
        if (DEBUG_TOGGLE)
            console.log(`[toggleCondition] mergeIfAdjacent 실패, Step 6 시작`)
        function findTopLevelIndex(target) {
            const directIdx = completeList.value.indexOf(target)
            if (directIdx !== -1) return directIdx

            for (let i = 0; i < completeList.value.length; i++) {
                const item = completeList.value[i]
                if (Array.isArray(item.group)) {
                    function hasTarget(node) {
                        if (node === target) return true
                        if (Array.isArray(node.group)) {
                            return node.group.some((child) => hasTarget(child))
                        }
                        return false
                    }

                    if (hasTarget(item)) {
                        return i
                    }
                }
            }

            return -1
        }

        const topItemIdx = findTopLevelIndex(topNode)
        const bottomItemIdx = findTopLevelIndex(bottomNode)
        if (DEBUG_TOGGLE)
            console.log(
                `[toggleCondition] topItemIdx=${topItemIdx}, bottomItemIdx=${bottomItemIdx}`
            )

        if (
            topItemIdx !== -1 &&
            bottomItemIdx !== -1 &&
            topItemIdx + 1 === bottomItemIdx
        ) {
            if (DEBUG_TOGGLE)
                console.debug(`[toggleCondition] 최상위 병합 성공`)
            const leftEntity = completeList.value[topItemIdx]
            const rightEntity = completeList.value[bottomItemIdx]
            newGroup.group = [leftEntity, rightEntity]
            completeList.value.splice(topItemIdx, 2, newGroup)
            replacedContainer = completeList.value
            replacedIndex = topItemIdx
            replaced = true
        }
    }

    if (DEBUG_TOGGLE) console.debug(`[toggleCondition] replaced=${replaced}`)

    if (replaced) {
        // ✅ 부모 그룹 ops 정리: 내부 결합된 커넥터(ops[replacedIndex])만 제거, 나머지 보존
        function findGroupNodeForChildren(
            childrenList,
            list = completeList.value
        ) {
            for (const item of list) {
                if (Array.isArray(item?.group)) {
                    if (item.group === childrenList) return item
                    const found = findGroupNodeForChildren(
                        item.group,
                        item.group
                    )
                    if (found) return found
                }
            }
            return null
        }
        if (replacedContainer && replacedIndex >= 0) {
            const parentGroupNode = findGroupNodeForChildren(replacedContainer)
            if (parentGroupNode && Array.isArray(parentGroupNode.ops)) {
                const oldOps = [...parentGroupNode.ops]
                if (replacedIndex < oldOps.length) {
                    oldOps.splice(replacedIndex, 1) // 내부 연결자 제거
                    parentGroupNode.ops = oldOps
                }
            }
        }

        if (DEBUG_TOGGLE)
            console.log(
                `[toggleCondition] depth 증가 시작 전: newGroup.depth=${newGroup.depth}`
            )
        function incrementDepth(node) {
            if (typeof node.depth === 'number') {
                node.depth += 1
            } else {
                node.depth = 1
            }
            if (Array.isArray(node.group)) {
                node.group.forEach((child) => incrementDepth(child))
            }
        }
        incrementDepth(newGroup)
        if (DEBUG_TOGGLE)
            console.log(
                `[toggleCondition] depth 증가 완료: newGroup.depth=${newGroup.depth}`
            )

        function collapseGroups(list) {
            const result = []
            for (let i = 0; i < list.length; i++) {
                const item = list[i]
                if (Array.isArray(item.group) && item.group.length === 1) {
                    const child = item.group[0]
                    if (Array.isArray(child.group)) {
                        child.group = collapseGroups(child.group)
                    }
                    result.push(child)
                } else if (Array.isArray(item.group)) {
                    item.group = collapseGroups(item.group)
                    result.push(item)
                } else {
                    result.push(item)
                }
            }
            return result
        }

        completeList.value = collapseGroups(completeList.value)
        if (DEBUG_TOGGLE) console.debug(`[toggleCondition] collapseGroups 완료`)
    }

    completeList.value = [...completeList.value]
    if (DEBUG_TOGGLE)
        console.debug(`[toggleCondition] 완료: completeList 재할당`)
    state._locked = false
    if (idx - 2 >= 0) {
        groupEntryButtons.value.add(idx - 2)
    }
    __printStructure(`AFTER toggleCondition idx=${idx}`)
}

/** ✅ moveLeft: AND의 역작동 (depth -1 + 그룹 정리) */
function moveLeft(idx) {
    __printStructure(`BEFORE moveLeft idx=${idx}`)
    const state = buttonStates.value[idx - 1] || null
    let didUnwrapOwning = false // 스코프(부모 그룹 내부)에서 래퍼 해제 발생
    let didUnwrapTopLevel = false // 최상위에서 래퍼 해제 발생

    const leftLeaf = flattenedList.value[idx - 1]
    const rightLeaf = flattenedList.value[idx]
    if (!leftLeaf || !rightLeaf) return

    // 헬퍼: __groupId로 그룹 찾기
    function findGroupById(groupId, list = completeList.value) {
        for (const item of list) {
            if (Array.isArray(item.group)) {
                if (item.__groupId === groupId) return item
                const found = findGroupById(groupId, item.group)
                if (found) return found
            }
        }
        return null
    }

    // 헬퍼: 엔티티가 리프를 포함하는지 확인
    function containsNode(entity, leaf) {
        if (entity === leaf) return true
        if (Array.isArray(entity?.group)) {
            for (const child of entity.group) {
                if (containsNode(child, leaf)) return true
            }
        }
        return false
    }

    // 커넥터 메타에서 스코프 컨테이너 결정
    const conn = connectorDepths.value[idx - 1]
    const scopeGroupId = conn?.parentGroupId || null
    let container = scopeGroupId
        ? findGroupById(scopeGroupId)?.group
        : completeList.value
    if (!container) container = completeList.value

    // 이 스코프에서 인접한 엔티티 찾기
    let pairIndex = -1
    if (scopeGroupId && typeof conn?._intraGroupIndex === 'number') {
        pairIndex = conn._intraGroupIndex
    } else {
        for (let i = 0; i < container.length - 1; i++) {
            const curr = container[i]
            const next = container[i + 1]
            if (
                (containsNode(curr, leftLeaf) &&
                    containsNode(next, rightLeaf)) ||
                (containsNode(curr, rightLeaf) && containsNode(next, leftLeaf))
            ) {
                pairIndex = i
                break
            }
        }
    }
    if (pairIndex < 0) return

    // 들여쓰기 감소 로직: 이 스코프의 소유 그룹의 들여쓰기를 우선 감소
    if (scopeGroupId) {
        const owningGroup = findGroupById(scopeGroupId)
        if (owningGroup) {
            owningGroup._indent = Math.max(
                0,
                Number(owningGroup._indent || 0) - 1
            )
            // ✅ 그룹 해제 조건: _indent가 0이면 연산자 종류와 무관하게 래퍼 제거(자식으로 치환)
            //    - 논리 보존: 기존 버튼 상태(buttonStates)는 그대로 유지되므로,
            //      펼쳐진 위치의 커넥터 연산자(예: OR)도 동일 인덱스에 남아 의미가 보존됩니다.
            if (Number(owningGroup._indent || 0) === 0) {
                if (DEBUG_TOGGLE)
                    console.log(
                        '[moveLeft] unwrap owningGroup: indent=0 → unwrap regardless of operator'
                    )
                // 부모 컨테이너에서 그룹을 자식들로 치환
                function findParentContainer(
                    target,
                    list = completeList.value
                ) {
                    for (let i = 0; i < list.length; i++) {
                        const item = list[i]
                        if (item === target) return { parent: list, index: i }
                        if (Array.isArray(item?.group)) {
                            const found = findParentContainer(
                                target,
                                item.group
                            )
                            if (found) return found
                        }
                    }
                    return null
                }
                const where = findParentContainer(owningGroup)
                if (where && Array.isArray(owningGroup.group)) {
                    // parentGroup 노드 찾기 (top-level이면 없음)
                    function findGroupNodeForChildren(
                        childrenList,
                        list = completeList.value
                    ) {
                        for (const item of list) {
                            if (Array.isArray(item?.group)) {
                                if (item.group === childrenList) return item
                                const found = findGroupNodeForChildren(
                                    item.group,
                                    item.group
                                )
                                if (found) return found
                            }
                        }
                        return null
                    }

                    const parentGroupNode = findGroupNodeForChildren(
                        where.parent
                    )
                    // 기존 parent ops의 owningGroup과 그 다음 항목 사이 operator를 보관 (있을 때)
                    const oldOpToNext =
                        parentGroupNode && Array.isArray(parentGroupNode.ops)
                            ? parentGroupNode.ops[where.index] // owningGroup와 다음 sibling 사이
                            : undefined

                    // 펼치기: owningGroup 위치에 자식들을 그대로 삽입
                    const insertedChildren = [...owningGroup.group]
                    where.parent.splice(where.index, 1, ...insertedChildren)
                    didUnwrapOwning = true

                    // parentGroup의 ops 재배열: 내부 자식들 사이 커넥터 + 기존 next 커넥터 보존
                    if (parentGroupNode && Array.isArray(parentGroupNode.ops)) {
                        const n = insertedChildren.length
                        const innerOps = Array.isArray(owningGroup.ops)
                            ? [...owningGroup.ops]
                            : []
                        // 컨텍스트 연산자 산정: next-op 우선 → prev-op → 내부 첫 op → 버튼 상태
                        let contextOp = oldOpToNext
                        if (contextOp === undefined && where.index - 1 >= 0) {
                            const prevOp = parentGroupNode.ops[where.index - 1]
                            if (prevOp !== undefined) contextOp = prevOp
                        }
                        if (contextOp === undefined) {
                            contextOp =
                                innerOps[0] || state?.conditionType || 'AND'
                        }
                        // 새로 들어온 자식들 사이 (n-1)개의 커넥터는 컨텍스트 연산자로 통일
                        const insertedOps = Array(Math.max(0, n - 1)).fill(
                            contextOp
                        )

                        const before = parentGroupNode.ops.slice(0, where.index)
                        const after = parentGroupNode.ops.slice(where.index + 1)
                        const merged = [
                            ...before,
                            ...insertedOps,
                            ...(oldOpToNext !== undefined ? [oldOpToNext] : []),
                            ...after
                        ]
                        parentGroupNode.ops = merged

                        // 클릭된 버튼도 컨텍스트 연산자로 동기화
                        if (state) {
                            state.conditionType = contextOp
                            buttonStates.value = [...buttonStates.value]
                        }
                    }
                }
            }
        }
    } else {
        // 최상위: 인접 엔티티의 들여쓰기 감소 시도
        const leftEntity = container[pairIndex]
        const rightEntity = container[pairIndex + 1]
        if (
            Array.isArray(leftEntity?.group) &&
            Number(leftEntity._indent || 0) > 0
        ) {
            leftEntity._indent = Number(leftEntity._indent || 0) - 1
        } else if (
            Array.isArray(rightEntity?.group) &&
            Number(rightEntity._indent || 0) > 0
        ) {
            rightEntity._indent = Number(rightEntity._indent || 0) - 1
        } else {
            // 줄일 항목 없음
        }

        // ✅ top-level에서도 _indent가 0이고 OR가 없는 그룹은 래퍼를 제거
        function unwrapIfPlainAndZeroIndent(entity, parentList, atIndex) {
            if (!Array.isArray(entity?.group)) return false
            const isZero = Number(entity._indent || 0) === 0
            if (isZero && Array.isArray(parentList)) {
                if (DEBUG_TOGGLE)
                    console.log(
                        '[moveLeft] unwrap top-level entity group: indent=0 → unwrap regardless of operator'
                    )
                parentList.splice(atIndex, 1, ...entity.group)
                return true
            }
            return false
        }
        // 왼쪽 또는 오른쪽 엔티티가 그룹이면 해제 시도
        if (Array.isArray(leftEntity?.group)) {
            if (unwrapIfPlainAndZeroIndent(leftEntity, container, pairIndex)) {
                didUnwrapTopLevel = true
            }
        }
        if (Array.isArray(rightEntity?.group)) {
            // 오른쪽은 인덱스가 하나 밀려있음을 고려
            const idxToUse =
                pairIndex +
                (Array.isArray(leftEntity?.group) ? leftEntity.group.length : 1)
            // 위에서 왼쪽이 먼저 풀리면 index가 바뀔 수 있으므로 재탐색로직으로 안전 조정
            // 간단히 최신 container에서 다시 위치를 찾는다
            const iNow = container.indexOf(rightEntity)
            if (iNow !== -1) {
                if (unwrapIfPlainAndZeroIndent(rightEntity, container, iNow)) {
                    didUnwrapTopLevel = true
                }
            }
        }
    }

    // 길이가 1인 그룹 래퍼 축소
    function collapseGroupsKeepingOrder(list) {
        const result = []
        for (const item of list) {
            if (Array.isArray(item.group)) {
                item.group = collapseGroupsKeepingOrder(item.group)
                if (item.group.length === 1) {
                    result.push(item.group[0])
                } else {
                    result.push(item)
                }
            } else {
                result.push(item)
            }
        }
        return result
    }

    completeList.value = collapseGroupsKeepingOrder(completeList.value)
    completeList.value = [...completeList.value]

    // ✅ top-level에서 래퍼가 해제된 경우에만 AND로 수렴(간단 규칙)
    if (didUnwrapTopLevel && state) {
        state.conditionType = 'AND'
        buttonStates.value = [...buttonStates.value]
    }

    if (state) state._locked = false
    groupEntryButtons.value.delete(idx - 2)
    __printStructure(`AFTER moveLeft idx=${idx}`)
}
let groupIdCounter = 0
const connectorDepths = ref([]) // [{ idx, depth }]
const preCalculatedButtonDepths = ref({}) // { btnIdx: depth } (반응성 보장)

/** ✅ flattenRecursive (pure depth: node.depth를 참조하지 않고, 인자 baseDepth만 사용) */
let completeIndexCounter = 0

function flattenRecursive(
    node,
    result,
    baseDepth = 0,
    parentGroupId = null,
    groupIndex = null,
    connectors = [],
    parentOp = null,
    entityPath = {},
    parentGroupSize = null
) {
    if (Array.isArray(node.group)) {
        const currentGroupId = `g${groupIdCounter++}`

        if (!Array.isArray(node.ops)) node.ops = []
        const need = Math.max(0, node.group.length - 1)
        while (node.ops.length < need) node.ops.push('AND')
        if (node.ops.length > need) node.ops.splice(need)

        // 🔹 depth 계산 규칙 (업데이트)
        // - AND/OR 여부는 깊이에 영향을 주지 않는다
        // - 오직 _indent만 깊이에 반영한다 (그룹의 시각적 들여쓰기)
        const add = Number(node?._indent || 0)
        const groupBaseDepth = baseDepth + add

        // ✅ 그룹 자체 정보 저장 (나중에 부모 커넥터 찾기용)
        node.__groupId = currentGroupId
        node.__parentGroupId = parentGroupId
        node.__groupIndexInParent = groupIndex
        node.__groupDepth = groupBaseDepth

        node.group.forEach((child, gi) => {
            flattenRecursive(
                child,
                result,
                groupBaseDepth,
                currentGroupId,
                gi,
                connectors,
                node.ops[gi - 1] || parentOp,
                { ...entityPath, [currentGroupId]: gi },
                node.group.length
            )

            // 🔹 같은 그룹 내 인접 child 사이 커넥터
            if (gi < node.group.length - 1) {
                connectors.push({
                    key: `${currentGroupId}_${gi}`,
                    operator: node.ops[gi] || 'AND',
                    // 🔹 OR 그룹이면 버튼도 들여쓰기
                    depth: groupBaseDepth,
                    parentGroupId: currentGroupId,
                    _intraGroupIndex: gi, // ✅ 그룹 내 몇 번째 커넥터인지 기록
                    _isGroupInternal: true,
                    _locked: false
                })
            }
        })

        // ✅ 부모 그룹에서 이 그룹 뒤로의 커넥터도 저장
        // (다음 그룹/노드로 전환할 때 사용)
        if (
            parentGroupId !== null &&
            groupIndex < /*parent children count*/ 999
        ) {
            // 부모 그룹의 인접 커넥터를 connectorList에 추가
            // 이건 부모에서 처리하므로 여기선 스킵
        }
    } else {
        node.__completeIndex = completeIndexCounter++
        node.__groupId = parentGroupId // 현재 노드가 속한 그룹
        node.__groupIndex = groupIndex
        // ✅ 소속 그룹의 마지막 인덱스 기록 (경계 판단용)
        node.__groupLastIndex =
            typeof parentGroupSize === 'number'
                ? Math.max(0, parentGroupSize - 1)
                : null
        node.depth = baseDepth
        node.__nodeRef = node // 원본 노드 참조 (group 속성 확인용)
        // ✅ 조상 그룹 스코프에서 이 리프가 속한 '엔티티(child index)'를 기록
        // 예: entityAt[gX] = k  (조상 그룹 gX에서 k번째 child 하위에 존재)
        try {
            node.__entityAt = { ...entityPath }
        } catch (e) {
            node.__entityAt = {}
        }
        result.push(node)
    }
}

/** ✅ flatten & 버튼 상태 동기화 */
watchEffect(
    () => {
        const result = []
        const connectorList = []
        groupIdCounter = 0
        completeIndexCounter = 0

        // 🔁 이전 프레임의 커넥터 key → 버튼 상태(AND/OR) 매핑 보존
        const prevConnectorStates = {}
        try {
            ;(connectorDepths.value || []).forEach((c, i) => {
                const key = c.key
                const prevState = buttonStates.value?.[i]?.conditionType
                // 'btn_' 키는 인덱스 기반으로 프레임마다 달라지므로 보존 대상에서 제외
                if (typeof key === 'string' && key.startsWith('btn_')) return
                prevConnectorStates[key] = prevState || c.operator || 'AND'
            })
        } catch (e) {}

        completeList.value.forEach((node) => {
            flattenRecursive(
                toRaw(node),
                result,
                0,
                null,
                null,
                connectorList,
                null,
                {}
            )
        })

        // ✅ 핵심: result 배열의 순서에 맞춰서 각 버튼 위치에 올바른 커넥터 배정
        const finalConnectorList = []

        // result[i]와 result[i+1] 사이에 있는 버튼이 finalConnectorList[i]
        for (let btnIdx = 0; btnIdx < result.length - 1; btnIdx++) {
            const currNode = result[btnIdx]
            const nextNode = result[btnIdx + 1]

            // 기본값: 일반(스코프 외) 커넥터 → 인접 리프 쌍 기반의 안정 키 사용
            const pairKey = `pair_${currNode.key}__${nextNode.key}`
            let buttonConnector = {
                key: pairKey,
                operator: null, // 기본값은 상태에서 가져오지 않는다(잘못된 인덱스 전파 방지)
                depth: 0,
                _locked: buttonStates.value[btnIdx]?._locked || false
            }

            // 🔹 FIRST PRIORITY: 미리 계산된 depth가 있으면 무조건 그것을 사용!
            // 📌 btnIdx는 0부터이므로, finalConnectorList 인덱스와 같음
            if (preCalculatedButtonDepths.value[btnIdx] !== undefined) {
                const preCalc = preCalculatedButtonDepths.value[btnIdx]
                const preCalcDepth =
                    typeof preCalc === 'object' ? preCalc.depth : preCalc
                buttonConnector.depth = preCalcDepth
                console.log(
                    `[버튼 ${btnIdx}] ⭐ 미리 계산된 depth 사용: ${preCalcDepth}`
                )
            } else if (
                currNode.__groupId !== null &&
                nextNode.__groupId !== null &&
                currNode.__groupId === nextNode.__groupId &&
                currNode.__groupIndex + 1 === nextNode.__groupIndex
            ) {
                // Case 1: 같은 그룹 내 인접한 노드 → 그룹 내부 커넥터 찾기
                const groupId = currNode.__groupId
                const intraIdx = currNode.__groupIndex
                const groupConn = connectorList.find(
                    (c) =>
                        c.parentGroupId === groupId &&
                        c._intraGroupIndex === intraIdx
                )
                if (groupConn) {
                    buttonConnector = groupConn
                }
            } else {
                // Case 2 & 3: 다른 그룹 또는 그룹과 일반 노드 혼합
                // 📌 보강: 공통 조상 그룹 스코프의 커넥터를 우선 매핑
                const leftMap = currNode.__entityAt || {}
                const rightMap = nextNode.__entityAt || {}
                const candidateGroupIds = Object.keys(leftMap).filter((k) =>
                    Object.prototype.hasOwnProperty.call(rightMap, k)
                )
                let pickedConn = null
                let pickedDepth = -1
                for (const gId of candidateGroupIds) {
                    const li = leftMap[gId]
                    const ri = rightMap[gId]
                    if (
                        typeof li === 'number' &&
                        typeof ri === 'number' &&
                        ri === li + 1
                    ) {
                        const found = connectorList.find(
                            (c) =>
                                c.parentGroupId === gId &&
                                c._intraGroupIndex === li
                        )
                        if (found) {
                            const d =
                                typeof found.depth === 'number'
                                    ? found.depth
                                    : 0
                            if (d >= pickedDepth) {
                                pickedConn = found
                                pickedDepth = d
                            }
                        }
                    }
                }
                if (pickedConn) {
                    buttonConnector = pickedConn
                } else {
                    // 기존 Depth 계산 로직 유지
                    const currDepth = currNode.depth ?? 0
                    const nextDepth = nextNode.depth ?? 0
                    const minDepth = Math.min(currDepth, nextDepth)

                    // 🔹 completeList에서 실제 원본 노드를 찾아서 group 존재 여부 판단
                    let currIsGroup = false
                    let nextIsGroup = false
                    let currIsLeaf = false
                    let nextIsLeaf = false

                    // currNode를 completeList에서 찾기
                    function findInCompleteList(nodeToFind) {
                        let foundType = null
                        function walk(arr) {
                            for (const item of arr) {
                                if (item && Array.isArray(item.group)) {
                                    if (item === nodeToFind) {
                                        foundType = 'group'
                                        return true
                                    }
                                    if (walk(item.group)) return true
                                } else if (item === nodeToFind) {
                                    foundType = 'leaf'
                                    return true
                                }
                            }
                            return false
                        }
                        walk(completeList.value || [])
                        return foundType
                    }
                    const currFound = findInCompleteList(currNode)
                    const nextFound = findInCompleteList(nextNode)
                    currIsGroup = currFound === 'group'
                    currIsLeaf = currFound === 'leaf'
                    nextIsGroup = nextFound === 'group'
                    nextIsLeaf = nextFound === 'leaf'
                    // ✅ 추가: 현재 노드가 속한 그룹의 마지막 leaf인지 여부 계산 (누락으로 ReferenceError 발생)
                    const currIsGroupLastLeaf =
                        currIsLeaf &&
                        currNode.__groupId !== null &&
                        typeof currNode.__groupIndex === 'number' &&
                        typeof currNode.__groupLastIndex === 'number' &&
                        currNode.__groupIndex === currNode.__groupLastIndex
                    const nextIsGroupFirstLeaf =
                        nextNode.__groupId !== null &&
                        nextNode.__groupIndex === 0 &&
                        nextIsLeaf

                    const isGroupBoundary =
                        currIsGroupLastLeaf &&
                        nextIsGroupFirstLeaf &&
                        currNode.__groupId !== nextNode.__groupId

                    let buttonDepth
                    if (isGroupBoundary) {
                        buttonDepth = Math.max(0, minDepth - 1)
                    } else if (currIsLeaf && nextIsLeaf) {
                        buttonDepth = minDepth
                    } else if (
                        (currIsLeaf && (currIsGroup || nextIsGroup)) ||
                        (nextIsLeaf && (currIsGroup || nextIsGroup))
                    ) {
                        buttonDepth = minDepth
                    } else if (currIsGroup && nextIsGroup) {
                        buttonDepth = Math.max(0, minDepth - 1)
                    } else {
                        buttonDepth = minDepth
                    }

                    buttonConnector.depth = buttonDepth

                    // ⭐ KEY FIX: preCalculatedButtonDepths에서 제거 (보강)
                    if (preCalculatedButtonDepths.value[btnIdx] !== undefined) {
                        delete preCalculatedButtonDepths.value[btnIdx]
                    }
                }
            }
            finalConnectorList[btnIdx] = buttonConnector
        }

        // flatten 결과 반영
        flattenedList.value = result

        // ✅ 버튼 상태 재구성: 커넥터 key 기준으로 이전 상태를 보존하여 재배치
        const need = Math.max(0, result.length - 1)
        const prevButtonStates = toRaw(buttonStates.value) || []
        const rebuiltStates = new Array(need).fill(null).map((_, i) => {
            const conn = finalConnectorList[i]
            const key = conn?.key
            let prev = key ? prevConnectorStates[key] : null
            // 'btn_' 키는 무시: 인덱스가 바뀌면 다른 커넥터로 잘못 매칭될 수 있음
            if (typeof key === 'string' && key.startsWith('btn_')) prev = null

            // 🔹 우선순위: 1) conn.operator (flattenRecursive에서 설정된 group ops)
            //             2) prev (이전 상태)
            //             3) conn.operator fallback
            //             4) 기본값 AND
            const cond =
                conn?.operator ||
                prev ||
                prevButtonStates?.[i]?.conditionType ||
                'AND'

            if (DEBUG_TOGGLE && (conn?.operator || prev)) {
                console.log(
                    `[버튼 ${i}] operator=${conn?.operator}, prev=${prev}, final=${cond}`
                )
            }

            return { conditionType: cond, _locked: false }
        })
        buttonStates.value = rebuiltStates
        // 🔹 그룹 내부 커넥터(parentGroupId 존재)는 반드시 해당 그룹 ops 값을 강제 적용
        try {
            finalConnectorList.forEach((conn, i) => {
                if (conn?.parentGroupId) {
                    // connectorList에서 이미 operator 세팅됨 → 직접 덮어쓰기
                    if (conn.operator)
                        buttonStates.value[i].conditionType = conn.operator
                }
            })
        } catch (e) {}
        // 반응성 재트리거
        buttonStates.value = [...buttonStates.value]

        // ✅ 버튼 인덱스-키 매핑 동기화 (라벨 표시 시 키 기반 매칭)
        buttonIndexKeyMap.value = finalConnectorList.map((c) => c?.key)
        renderConnectorList.value = finalConnectorList.map((c) => ({
            key: c.key,
            operator: c.operator,
            depth: c.depth,
            parentGroupId: c.parentGroupId
        }))

        // connector depth 반영
        // 🔹 finalConnectorList의 값을 우선 사용 (preCalculatedButtonDepths 포함)
        // 만약 finalConnectorList에서 계산된 depth가 없으면 기존값 보존
        const existingDepthMap = {}
        connectorDepths.value.forEach((item) => {
            existingDepthMap[item.key] = item.depth
        })

        const updatedConnectorDepths = finalConnectorList.map((item) => {
            return {
                ...item,
                depth:
                    item.depth !== undefined
                        ? item.depth // ✅ finalConnectorList의 계산된 값 우선 사용
                        : existingDepthMap[item.key] // 백업: 기존값
            }
        })
        connectorDepths.value = updatedConnectorDepths

        // ✅ 최상위(depth=0) 커넥터는 항상 AND 규칙 강제
        let topLevelFixed = false
        for (let i = 0; i < buttonStates.value.length; i++) {
            const d = connectorDepths.value[i]?.depth ?? 0
            if (d === 0 && buttonStates.value[i]?.conditionType !== 'AND') {
                if (DEBUG_TOGGLE) {
                    const key = connectorDepths.value[i]?.key
                    const before = buttonStates.value[i]?.conditionType
                    console.log(
                        `[ENFORCE] depth=0 강제 AND: idx=${i}, key=${key}, before=${before}`
                    )
                }
                buttonStates.value[i].conditionType = 'AND'
                topLevelFixed = true
            }
        }
        if (topLevelFixed) {
            // 반응성 갱신
            buttonStates.value = [...buttonStates.value]
        }

        // 🔹 watchEffect 완료 후, preCalculatedButtonDepths 초기화
        // (이렇게 하면 다음 버튼 클릭 시 새로운 값이 들어올 수 있음)
        preCalculatedButtonDepths.value = {}
    },
    { flush: 'post' } // ✅ post로 변경: toggleCondition 완료 후 실행
)

/** ✅ margin 계산: connectorDepths 기반 들여쓰기 */
function getConnectorIndentPx(idx) {
    const conn = connectorDepths.value[idx - 1]
    const indent = conn ? `${conn.depth * 30}px` : '0px'
    return indent
}
</script>
