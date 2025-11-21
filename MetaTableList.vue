<template>
    <!-- Container -->
    <div
        id="kt_content_container"
        class="d-flex flex-column-fluid align-items-stretch h-admin"
    >
        <div
            class="wrapper d-flex flex-column flex-row-fluid mt-4 h-admin"
            id="kt_wrapper"
        >
            <div class="content flex-column-fluid h-admin" id="kt_content">
                <div class="px-4">
                    <div class="row gy-3 g-xl-4 h-xl-100">
                        <!-- 메타 테이블 정보 카드 -->
                        <div class="col-12">
                            <div
                                class="accordion card card-bordered"
                                id="kt_accordion_1"
                            >
                                <div
                                    class="accordion-item border-0 bg-transparent"
                                >
                                    <!-- 헤더 타이틀 -->
                                    <div
                                        class="accordion-header card-header align-items-center"
                                        id="kt_accordion_1_header_1"
                                    >
                                        <div
                                            class="row align-items-center w-lg-75"
                                        >
                                            <div
                                                class="col-auto fs-4 fw-bolder"
                                            >
                                                메타 테이블 이름
                                            </div>
                                        </div>
                                        <div class="card-toolbar">
                                            <button
                                                id="meta_table_collapse"
                                                class="accordion-button fs-4 fw-bold bg-light shadow-none rounded-circle"
                                                type="button"
                                                @click="toggleAccordion"
                                                :aria-expanded="isAccordionOpen"
                                            ></button>
                                        </div>
                                    </div>

                                    <!-- 검색 조건 -->
                                    <div
                                        class="accordion-header card-header align-items-center"
                                        style="cursor: default"
                                    >
                                        <div
                                            class="row align-items-center ms-1"
                                        >
                                            <div class="w-75px ta-right">
                                                활성 여부
                                            </div>
                                            <div class="w-150px">
                                                <select
                                                    v-model="
                                                        searchCondition.status
                                                    "
                                                    @change="
                                                        selectMetaTableList
                                                    "
                                                    class="form-select form-select-sm"
                                                >
                                                    <option value="all">
                                                        전체
                                                    </option>
                                                    <option value="active">
                                                        활성화
                                                    </option>
                                                    <option value="inactive">
                                                        비활성화
                                                    </option>
                                                </select>
                                            </div>
                                            <div class="w-90px ta-right">
                                                테이블 타입
                                            </div>
                                            <div class="w-150px">
                                                <select
                                                    v-model="
                                                        searchCondition.type
                                                    "
                                                    @change="
                                                        selectMetaTableList
                                                    "
                                                    class="form-select form-select-sm"
                                                >
                                                    <option value="all">
                                                        전체
                                                    </option>
                                                    <option value="mt">
                                                        일반 테이블(MT)
                                                    </option>
                                                    <option value="vt">
                                                        복제 테이블(VT)
                                                    </option>
                                                </select>
                                            </div>
                                            <div class="w-75px ta-right">
                                                테이블명
                                            </div>
                                            <div class="w-250px">
                                                <form
                                                    class="position-relative"
                                                    style="margin-bottom: 0px"
                                                    @submit.prevent="
                                                        selectMetaTableList
                                                    "
                                                >
                                                    <input
                                                        v-model="
                                                            searchCondition.tableName
                                                        "
                                                        type="text"
                                                        class="form-control form-control-sm pe-11"
                                                        placeholder="찾으실 테이블명을 입력하세요."
                                                        @keydown.enter="
                                                            selectMetaTableList
                                                        "
                                                    />
                                                    <a
                                                        @click="
                                                            selectMetaTableList
                                                        "
                                                        class="cursor-pointer"
                                                    >
                                                        <span
                                                            class="position-absolute top-50 end-0 translate-middle-y me-4"
                                                        >
                                                            <i
                                                                class="ri-search-line text-dark fs-3"
                                                            ></i>
                                                        </span>
                                                    </a>
                                                </form>
                                            </div>
                                            <div class="w-90px ta-right">
                                                테이블 목록
                                            </div>
                                            <div class="w-300px">
                                                <select
                                                    v-model="selectedTableId"
                                                    @change="onTableSelect"
                                                    class="form-select form-select-sm"
                                                >
                                                    <option
                                                        v-for="table in tableList"
                                                        :key="table.id"
                                                        :value="table.id"
                                                    >
                                                        {{ table.name }}
                                                    </option>
                                                </select>
                                            </div>
                                            <div class="w-50px mt-1">
                                                <a
                                                    @click="initSearchCondition"
                                                    title="검색조건 초기화"
                                                    class="cursor-pointer"
                                                >
                                                    <i
                                                        class="ri-refresh-line text-dark fs-2 mt-1"
                                                    ></i>
                                                </a>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- 테이블 상세 정보 -->
                                    <div
                                        v-show="isAccordionOpen"
                                        id="kt_accordion_1_body_1"
                                        class="accordion-collapse collapse show"
                                    >
                                        <div class="accordion-body">
                                            <div class="row gx-10 gy-6">
                                                <!-- 왼쪽 컬럼 -->
                                                <div
                                                    class="col-lg-4 border-1 border-end-dashed border-gray-400"
                                                >
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >메타 테이블
                                                            아이디</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            {{
                                                                metaTableForm.metaTableId
                                                            }}
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >메타 테이블 영문
                                                            이름</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            {{
                                                                metaTableForm.metaTable
                                                            }}
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >메타 테이블 한글
                                                            이름</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            <input
                                                                v-model="
                                                                    metaTableForm.metaTableName
                                                                "
                                                                type="text"
                                                                class="form-control form-control-sm"
                                                                @input="
                                                                    onMetaTableChange
                                                                "
                                                            />
                                                        </div>
                                                    </div>
                                                </div>

                                                <!-- 중간 컬럼 -->
                                                <div
                                                    class="col-lg-4 border-1 border-end-dashed border-gray-400"
                                                >
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >파티션 키</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            <input
                                                                v-model="
                                                                    metaTableForm.partitionKey
                                                                "
                                                                type="text"
                                                                class="form-control form-control-sm"
                                                                @input="
                                                                    onMetaTableChange
                                                                "
                                                            />
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >메타 테이블
                                                            활성상태</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 d-flex mt-0"
                                                        >
                                                            <div
                                                                class="form-check form-check-custom form-check-solid me-5"
                                                            >
                                                                <input
                                                                    v-model="
                                                                        metaTableForm.status
                                                                    "
                                                                    class="form-check-input"
                                                                    type="radio"
                                                                    value="active"
                                                                    id="table_status_enabled"
                                                                    @change="
                                                                        onMetaTableChange
                                                                    "
                                                                />
                                                                <label
                                                                    class="form-check-label"
                                                                    for="table_status_enabled"
                                                                    >활성화</label
                                                                >
                                                            </div>
                                                            <div
                                                                class="form-check form-check-custom form-check-solid"
                                                            >
                                                                <input
                                                                    v-model="
                                                                        metaTableForm.status
                                                                    "
                                                                    class="form-check-input"
                                                                    type="radio"
                                                                    value="inactive"
                                                                    id="table_status_disabled"
                                                                    @change="
                                                                        onMetaTableChange
                                                                    "
                                                                />
                                                                <label
                                                                    class="form-check-label"
                                                                    for="table_status_disabled"
                                                                    >비활성화</label
                                                                >
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >메타 테이블 소유자
                                                            타입</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            {{
                                                                metaTableForm.metaOwnerType
                                                            }}
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >관점
                                                            생성요청</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            <div
                                                                class="form-check form-check-custom form-check-solid"
                                                            >
                                                                <a
                                                                    @click="
                                                                        selectDimensionList
                                                                    "
                                                                    class="btn btn-light pulse pulse-white me-1 padding-btn dimension-btn-ms-l"
                                                                >
                                                                    <i
                                                                        class="ri-server-line fs-3"
                                                                    ></i
                                                                    >관점
                                                                    생성요청
                                                                </a>
                                                                <a
                                                                    @click="
                                                                        showDimensionQueueResult
                                                                    "
                                                                    class="btn btn-light pulse pulse-white me-1 padding-btn"
                                                                >
                                                                    <i
                                                                        class="ri-file-list-3-line fs-3"
                                                                    ></i
                                                                    >관점
                                                                    생성결과
                                                                </a>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>

                                                <!-- 오른쪽 컬럼 -->
                                                <div class="col-lg-4">
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >등록 일시</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            {{
                                                                metaTableForm.regDate
                                                            }}
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >변경 일시</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            {{
                                                                metaTableForm.changDate
                                                            }}
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >생성자
                                                            아이디</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            {{
                                                                metaTableForm.regId
                                                            }}
                                                        </div>
                                                    </div>
                                                    <div
                                                        class="row g-2 align-items-center pb-3"
                                                    >
                                                        <label
                                                            class="col-4 col-lg-5 form-label text-muted"
                                                            >수정자
                                                            아이디</label
                                                        >
                                                        <div
                                                            class="col-8 col-lg-7 mt-0"
                                                        >
                                                            {{
                                                                metaTableForm.changId
                                                            }}
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>

                                    <!-- Footer 버튼 -->
                                    <div class="card-footer text-end py-3">
                                        <a
                                            @click="showCopyMetaTableModal"
                                            class="btn btn-light cursor-pointer"
                                        >
                                            <i
                                                class="ri-file-copy-line fs-3"
                                            ></i
                                            >테이블 복제
                                        </a>
                                        <a
                                            v-show="showDeleteBtn"
                                            @click="showDropMetaTableModal"
                                            class="btn btn-light-danger cursor-pointer"
                                        >
                                            <i
                                                class="ri-delete-bin-line fs-3"
                                            ></i
                                            >테이블 삭제
                                        </a>
                                        <a
                                            @click="updateMetaTable"
                                            class="btn btn-primary pulse pulse-white cursor-pointer"
                                        >
                                            <i class="ri-save-line fs-3"></i
                                            >저장
                                        </a>
                                        <div
                                            class="toastr-position-meta-table mt-20 me-4 position-absolute z-index-3"
                                        >
                                            <div
                                                v-show="hasMetaTableChange"
                                                class="toastr toastr-error"
                                                aria-live="polite"
                                            >
                                                <div class="toastr-message">
                                                    수정사항이 있습니다.
                                                    저장하려면 변경사항 저장
                                                    버튼을 눌러주세요!
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- 필드 관리 카드 -->
                        <div class="col-12">
                            <div class="card card-bordered">
                                <!-- 카드 헤더 -->
                                <div class="card-header">
                                    <div class="card-title fs-5">
                                        <span>선택한 테이블 내 필드</span>
                                    </div>
                                    <div class="card-toolbar">
                                        <a
                                            @click="showAddMetaFieldModal"
                                            class="btn btn-primary pulse pulse-white me-1 cursor-pointer"
                                        >
                                            <i class="ri-add-box-line fs-3"></i
                                            >새 필드 추가
                                        </a>
                                        <a
                                            @click="showEditMetaFieldInfoModal"
                                            class="btn btn-primary pulse pulse-white me-1 cursor-pointer"
                                        >
                                            <i class="ri-edit-box-line fs-3"></i
                                            >필드 속성 일괄변경
                                        </a>
                                        <a
                                            @click="updateMetaField"
                                            class="btn btn-primary pulse pulse-white cursor-pointer"
                                        >
                                            <i
                                                class="ri-file-copy-line fs-3"
                                            ></i
                                            >저장
                                        </a>
                                        <div
                                            class="toastr-position-meta-field mt-20 me-4 position-absolute z-index-3"
                                        >
                                            <div
                                                v-show="hasMetaFieldChange"
                                                class="toastr toastr-error"
                                                aria-live="polite"
                                            >
                                                <div class="toastr-message">
                                                    수정사항이 있습니다.
                                                    저장하려면 변경사항 저장
                                                    버튼을 눌러주세요!
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>

                                <!-- 카드 본문 -->
                                <div class="card-body">
                                    <div class="row gy-3 g-xl-4 h-xl-100">
                                        <!-- 왼쪽: 필드 트리 -->
                                        <div class="col-lg-5 col-xl-4">
                                            <div class="card card-bordered">
                                                <fieldset>
                                                    <div
                                                        class="input-icon input-icon-right w-100 px-5 py-3"
                                                    >
                                                        <form
                                                            class="position-relative"
                                                            style="
                                                                margin-bottom: 0px;
                                                            "
                                                            @submit.prevent="
                                                                onFieldSearch
                                                            "
                                                        >
                                                            <input
                                                                v-model="
                                                                    fieldSearchWord
                                                                "
                                                                type="text"
                                                                class="form-control form-control-sm pe-11"
                                                                placeholder="찾으실 필드명을 입력하세요."
                                                                @keydown.enter.prevent="
                                                                    onFieldSearch
                                                                "
                                                            />
                                                            <a
                                                                @click="
                                                                    onFieldSearch
                                                                "
                                                                class="cursor-pointer"
                                                            >
                                                                <span
                                                                    class="position-absolute top-50 end-0 translate-middle-y me-4"
                                                                >
                                                                    <i
                                                                        class="ri-search-line text-dark fs-3"
                                                                    ></i>
                                                                </span>
                                                            </a>
                                                        </form>
                                                    </div>
                                                    <div
                                                        class="hstack gap-1 px-5 pb-2"
                                                    >
                                                        <button
                                                            type="button"
                                                            class="btn btn-light btn-sm btn-icon"
                                                            @click="
                                                                expandAllFields
                                                            "
                                                        >
                                                            <i
                                                                class="ri-add-line"
                                                            ></i>
                                                        </button>
                                                        <button
                                                            type="button"
                                                            class="btn btn-light btn-sm btn-icon"
                                                            @click="
                                                                collapseAllFields
                                                            "
                                                        >
                                                            <i
                                                                class="ri-subtract-line"
                                                            ></i>
                                                        </button>
                                                    </div>
                                                </fieldset>
                                                <Simplebar
                                                    class="px-6"
                                                    style="max-height: 388px"
                                                >
                                                    <AntTree
                                                        v-if="
                                                            fieldTreeData &&
                                                            fieldTreeData.length >
                                                                0
                                                        "
                                                        :tree-data="
                                                            displayFieldList
                                                        "
                                                        :search-text="
                                                            appliedFieldSearch
                                                        "
                                                        :checked-field="false"
                                                        :api-keys="[]"
                                                        :expanded-keys="
                                                            fieldExpandedKeys
                                                        "
                                                        @update:expanded-keys="
                                                            (keys) =>
                                                                (fieldExpandedKeys =
                                                                    keys)
                                                        "
                                                        @node-drag-start="
                                                            onFieldSelect
                                                        "
                                                    />
                                                    <div
                                                        v-else
                                                        class="text-center text-muted py-5"
                                                    >
                                                        필드 정보가 없습니다.
                                                    </div>
                                                </Simplebar>
                                            </div>
                                        </div>

                                        <!-- 오른쪽: 필드 상세 정보 -->
                                        <div class="col-lg-7 col-xl-8">
                                            <div class="card card-bordered">
                                                <div class="card-body p-4">
                                                    <div class="row gx-10 gy-3">
                                                        <!-- 왼쪽 컬럼 -->
                                                        <div
                                                            class="col-xl-6 border-1 border-end-dashed border-gray-400"
                                                        >
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    아이디</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.metaFieldId ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    활성
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0 d-flex"
                                                                >
                                                                    <div
                                                                        class="form-check form-check-custom form-check-solid me-5"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.activeYn
                                                                            "
                                                                            class="form-check-input"
                                                                            type="radio"
                                                                            value="Y"
                                                                            id="field_status_enabled"
                                                                            @change="
                                                                                onMetaFieldChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="field_status_enabled"
                                                                            >활성화</label
                                                                        >
                                                                    </div>
                                                                    <div
                                                                        class="form-check form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.activeYn
                                                                            "
                                                                            class="form-check-input"
                                                                            type="radio"
                                                                            value="N"
                                                                            id="field_status_disabled"
                                                                            @change="
                                                                                onMetaFieldChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="field_status_disabled"
                                                                            >비활성화</label
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>

                                                            <div
                                                                class="separator separator-dashed pt-1 mb-3"
                                                            ></div>

                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    데이터타입</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.dataType ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    이름</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.metaField ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    한글
                                                                    이름</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <input
                                                                        v-model="
                                                                            metaFieldForm.metaFieldName
                                                                        "
                                                                        type="text"
                                                                        class="form-control form-control-sm"
                                                                        @input="
                                                                            onMetaFieldChange
                                                                        "
                                                                    />
                                                                </div>
                                                            </div>

                                                            <div
                                                                class="separator separator-dashed pt-1 mb-3"
                                                            ></div>

                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    마스크
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <div
                                                                        class="form-check form-switch form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.maskYn
                                                                            "
                                                                            class="form-check-input h-20px w-30px"
                                                                            type="checkbox"
                                                                            id="admin_meta_field_form_meta_field_mask_yn"
                                                                            @change="
                                                                                onMetaFieldChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="admin_meta_field_form_meta_field_mask_yn"
                                                                            >Yes
                                                                            /
                                                                            No</label
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    마스크
                                                                    타입</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <input
                                                                        v-model="
                                                                            metaFieldForm.maskType
                                                                        "
                                                                        type="text"
                                                                        class="form-control form-control-sm"
                                                                        @input="
                                                                            onMetaFieldChange
                                                                        "
                                                                    />
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    정보 보안
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <div
                                                                        class="form-check form-switch form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.infoSecurYn
                                                                            "
                                                                            class="form-check-input h-20px w-30px"
                                                                            type="checkbox"
                                                                            id="admin_meta_field_form_info_secur_yn"
                                                                            @change="
                                                                                onMetaFieldChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="admin_meta_field_form_info_secur_yn"
                                                                            >Yes
                                                                            /
                                                                            No</label
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>

                                                            <div
                                                                class="separator separator-dashed pt-1 mb-3"
                                                            ></div>

                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >관점
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <div
                                                                        class="form-check form-switch form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.dimensionYn
                                                                            "
                                                                            class="form-check-input h-20px w-30px"
                                                                            type="checkbox"
                                                                            id="admin_meta_field_form_meta_dimension_yn"
                                                                            @change="
                                                                                onDimensionChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="admin_meta_field_form_meta_dimension_yn"
                                                                            >Yes
                                                                            /
                                                                            No</label
                                                                        >
                                                                        <span
                                                                            class="ms-6"
                                                                            >{{
                                                                                metaFieldForm.dimensionCretDay
                                                                            }}</span
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >bidw 관점
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <div
                                                                        class="form-check form-switch form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.bidwDimensionYn
                                                                            "
                                                                            class="form-check-input h-20px w-30px"
                                                                            type="checkbox"
                                                                            id="admin_meta_field_form_bidw_meta_dimension_yn"
                                                                            @change="
                                                                                onDimensionChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="admin_meta_field_form_bidw_meta_dimension_yn"
                                                                            >Yes
                                                                            /
                                                                            No</label
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >관점 최근
                                                                    업데이트</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.dimensionDay ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                        </div>

                                                        <!-- 오른쪽 컬럼 -->
                                                        <div class="col-xl-6">
                                                            <div
                                                                class="separator separator-dashed pt-1 mb-3"
                                                            ></div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >메타 필드
                                                                    정보</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <input
                                                                        v-model="
                                                                            metaFieldForm.comment
                                                                        "
                                                                        type="text"
                                                                        class="form-control form-control-sm"
                                                                        @input="
                                                                            onMetaFieldChange
                                                                        "
                                                                    />
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >이미지
                                                                    업로드</label
                                                                >
                                                                <div
                                                                    class="col-4"
                                                                >
                                                                    <input
                                                                        v-model="
                                                                            metaFieldForm.imgPath
                                                                        "
                                                                        type="text"
                                                                        class="form-control form-control-sm"
                                                                        readonly
                                                                    />
                                                                </div>
                                                                <div
                                                                    class="col-3"
                                                                >
                                                                    <label
                                                                        for="meta_field_img_upload"
                                                                        class="cursor-pointer"
                                                                    >
                                                                        <span
                                                                            class="btn btn-primary btn-sm"
                                                                            style="
                                                                                padding: 0.3846rem
                                                                                    1.2rem;
                                                                            "
                                                                        >
                                                                            <i
                                                                                class="la la-upload icon-md"
                                                                            ></i
                                                                            >업로드
                                                                        </span>
                                                                    </label>
                                                                    <input
                                                                        id="meta_field_img_upload"
                                                                        type="file"
                                                                        accept=".png"
                                                                        style="
                                                                            display: none;
                                                                        "
                                                                        @change="
                                                                            handleFieldImageUpload
                                                                        "
                                                                    />
                                                                </div>
                                                            </div>

                                                            <div
                                                                class="separator separator-dashed pt-1 mb-3"
                                                            ></div>

                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >expert모드
                                                                    필수설정
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <div
                                                                        class="form-check form-switch form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.requiredYn
                                                                            "
                                                                            class="form-check-input h-20px w-30px"
                                                                            type="checkbox"
                                                                            id="admin_meta_field_form_meta_field_required_yn"
                                                                            @change="
                                                                                onMetaFieldChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="admin_meta_field_form_meta_field_required_yn"
                                                                            >Yes
                                                                            /
                                                                            No</label
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >easy모드
                                                                    조건
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <div
                                                                        class="form-check form-switch form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.easyConditionYn
                                                                            "
                                                                            class="form-check-input h-20px w-30px"
                                                                            type="checkbox"
                                                                            id="admin_meta_field_form_meta_easy_condition_yn"
                                                                            @change="
                                                                                onMetaFieldChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="admin_meta_field_form_meta_easy_condition_yn"
                                                                            >Yes
                                                                            /
                                                                            No</label
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >easy모드
                                                                    출력
                                                                    여부</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <div
                                                                        class="form-check form-switch form-check-custom form-check-solid"
                                                                    >
                                                                        <input
                                                                            v-model="
                                                                                metaFieldForm.easyItemYn
                                                                            "
                                                                            class="form-check-input h-20px w-30px"
                                                                            type="checkbox"
                                                                            id="admin_meta_field_form_meta_easy_item_yn"
                                                                            @change="
                                                                                onMetaFieldChange
                                                                            "
                                                                        />
                                                                        <label
                                                                            class="form-check-label"
                                                                            for="admin_meta_field_form_meta_easy_item_yn"
                                                                            >Yes
                                                                            /
                                                                            No</label
                                                                        >
                                                                    </div>
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >easy모드
                                                                    분류</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    <input
                                                                        v-model="
                                                                            metaFieldForm.easyCatalogue
                                                                        "
                                                                        type="text"
                                                                        class="form-control form-control-sm"
                                                                        @input="
                                                                            onMetaFieldChange
                                                                        "
                                                                    />
                                                                </div>
                                                            </div>

                                                            <div
                                                                class="separator separator-dashed pt-1 mb-3"
                                                            ></div>

                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >등록
                                                                    일시</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.regDate ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >변경
                                                                    일시</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.changDate ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >생성자
                                                                    아이디</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.regId ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                            <div
                                                                class="row g-2 align-items-center pb-3"
                                                            >
                                                                <label
                                                                    class="col-5 form-label text-muted"
                                                                    >수정자
                                                                    아이디</label
                                                                >
                                                                <div
                                                                    class="col-8 col-lg-7 mt-0"
                                                                >
                                                                    {{
                                                                        metaFieldForm.changId ||
                                                                        '-'
                                                                    }}
                                                                </div>
                                                            </div>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- Modal: 관점 목록 -->
    <DimensionListModal
        v-model="showDimensionListModal"
        :table-id="selectedTableId"
        @save="onDimensionSave"
    />

    <!-- Modal: 관점 생성 결과 -->
    <DimensionQueueResultModal v-model="showDimensionQueueResultModal" />

    <!-- Modal: 테이블 복제 -->
    <CopyMetaTableModal
        v-model="showCopyTableModal"
        :original-table-data="metaTableForm"
        @save="onTableCopy"
    />

    <!-- Modal: 테이블 삭제 -->
    <DropMetaTableModal
        v-model="showDropTableModal"
        :table-id="selectedTableId"
        @delete="onTableDelete"
    />

    <!-- Modal: 필드 추가 -->
    <AddMetaFieldModal
        v-model="showAddFieldModal"
        :table-id="selectedTableId"
        @save="onFieldAdd"
    />

    <!-- Modal: 필드 속성 일괄 변경 -->
    <EditMetaFieldInfoModal
        v-model="showEditFieldInfoModal"
        :fields="fieldTreeData"
        @save="onFieldBatchUpdate"
    />
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch } from 'vue'
import Simplebar from 'simplebar-vue'
import AntTree from '@/components/expert/AntTree.vue'
import DimensionListModal from './DimensionListModal.vue'
import DimensionQueueResultModal from './DimensionQueueResultModal.vue'
import CopyMetaTableModal from './CopyMetaTableModal.vue'
import DropMetaTableModal from './DropMetaTableModal.vue'
import AddMetaFieldModal from './AddMetaFieldModal.vue'
import EditMetaFieldInfoModal from './EditMetaFieldInfoModal.vue'
// import instance from '@/assets/js/GlobalAxios'

/**
 * 메타 테이블 관리 페이지
 * - 원본: trunk/abc-tgt/src/main/webapp/WEB-INF/views/abctgt/admin/meta/list.jsp
 * - 변환: Vue3 Composition API
 */

// ===== 검색 조건 =====
const searchCondition = reactive({
    status: 'all',
    type: 'all',
    tableName: ''
})

// ===== 테이블 목록 =====
const tableList = ref([])
const selectedTableId = ref(null)

// ===== 아코디언 상태 =====
const isAccordionOpen = ref(true)

// ===== 메타 테이블 폼 데이터 =====
const metaTableForm = reactive({
    metaTableId: '',
    metaTable: '',
    metaTableName: '',
    partitionKey: '',
    status: 'active',
    metaOwnerType: 'model',
    regDate: '',
    changDate: '',
    regId: '',
    changId: ''
})

// ===== 변경 감지 =====
const hasMetaTableChange = ref(false)
const showDeleteBtn = ref(false)

// ===== 필드 트리 데이터 =====
const fieldTreeData = ref([])
const originalFieldTreeData = ref([]) // 원본 트리 데이터 (변경 감지용)
const fieldSearchWord = ref('')
const appliedFieldSearch = ref('')
const fieldExpandedKeys = ref([])

// ===== 메타 필드 폼 데이터 =====
const metaFieldForm = reactive({
    metaFieldId: '',
    activeYn: 'Y',
    dataType: '',
    metaField: '',
    metaFieldName: '',
    maskYn: false,
    maskType: '',
    infoSecurYn: false,
    dimensionYn: false,
    bidwDimensionYn: false,
    dimensionCretDay: '',
    dimensionDay: '',
    comment: '',
    imgPath: '',
    requiredYn: false,
    easyConditionYn: false,
    easyItemYn: false,
    easyCatalogue: '',
    regDate: '',
    changDate: '',
    regId: '',
    changId: ''
})

// ===== 필드 변경 감지 =====
const hasMetaFieldChange = ref(false)

// ===== 모달 상태 =====
const showDimensionListModal = ref(false)
const showDimensionQueueResultModal = ref(false)
const showCopyTableModal = ref(false)
const showDropTableModal = ref(false)
const showAddFieldModal = ref(false)
const showEditFieldInfoModal = ref(false)

// ===== 필드 트리 관련 computed =====
const displayFieldList = computed(() => {
    if (!Array.isArray(fieldTreeData.value)) return []

    const query = appliedFieldSearch.value
    if (!query) return fieldTreeData.value

    return filterByTitle(fieldTreeData.value, query)
})

// ===== Methods =====

/**
 * 아코디언 토글
 */
const toggleAccordion = () => {
    isAccordionOpen.value = !isAccordionOpen.value
}

/**
 * 검색 조건 초기화
 */
const initSearchCondition = () => {
    searchCondition.status = 'all'
    searchCondition.type = 'all'
    searchCondition.tableName = ''
    selectMetaTableList()
}

/**
 * 메타 테이블 목록 조회
 */
const selectMetaTableList = async () => {
    try {
        // TODO: API 호출
        // const response = await instance.post('/api/admin/meta/table/list', searchCondition)
        // tableList.value = response.data

        // 임시 데이터
        tableList.value = [
            { id: 1, name: 'DEV_TEST_TABLE_01' },
            { id: 2, name: 'DEV_TEST_TABLE_02' }
        ]
    } catch (error) {
        console.error('메타 테이블 목록 조회 오류:', error)
    }
}

/**
 * 테이블 선택
 */
const onTableSelect = () => {
    showMetaTableInfo()
    loadFieldTree()
}

/**
 * 메타 테이블 정보 조회
 */
const showMetaTableInfo = async () => {
    if (!selectedTableId.value) return

    try {
        // TODO: API 호출
        // const response = await instance.get(`/api/admin/meta/table/${selectedTableId.value}`)
        // Object.assign(metaTableForm, response.data)

        // 임시 데이터
        Object.assign(metaTableForm, {
            metaTableId: 'MT001',
            metaTable: 'dev_test_table_01',
            metaTableName: 'DEV_TEST_TABLE_01',
            partitionKey: 'partition_key',
            status: 'active',
            metaOwnerType: 'model',
            regDate: '2025-01-01 10:00:00',
            changDate: '2025-01-15 14:30:00',
            regId: 'admin',
            changId: 'admin'
        })

        hasMetaTableChange.value = false
    } catch (error) {
        console.error('메타 테이블 정보 조회 오류:', error)
    }
}

/**
 * 필드 트리 데이터 로드
 */
const loadFieldTree = async () => {
    if (!selectedTableId.value) return

    try {
        // TODO: API 호출
        // const response = await instance.get(`/api/admin/meta/field/tree/${selectedTableId.value}`)
        // fieldTreeData.value = response.data

        // 임시 데이터 (JSTree 형식과 유사한 구조)
        fieldTreeData.value = [
            {
                key: 'folder1',
                title: '기본 정보',
                children: [
                    {
                        key: 'MF001',
                        title: '고객명',
                        metaFieldDataType: 'string',
                        metaIconType: 'word',
                        metaFieldId: 'MF001'
                    },
                    {
                        key: 'MF002',
                        title: '고객번호',
                        metaFieldDataType: 'string',
                        metaIconType: 'number',
                        metaFieldId: 'MF002'
                    }
                ]
            },
            {
                key: 'folder2',
                title: '상세 정보',
                children: [
                    {
                        key: 'MF003',
                        title: '주소',
                        metaFieldDataType: 'string',
                        metaIconType: 'word',
                        metaFieldId: 'MF003'
                    }
                ]
            }
        ]

        // 원본 데이터 저장 (깊은 복사)
        originalFieldTreeData.value = JSON.parse(
            JSON.stringify(fieldTreeData.value)
        )
    } catch (error) {
        console.error('필드 트리 조회 오류:', error)
    }
}

/**
 * 제목 기반 필터
 */
const filterByTitle = (nodes, keyword) => {
    const matchNode = (node) =>
        node.title.toLowerCase().includes(keyword.toLowerCase()) ||
        (node.children && node.children.some(matchNode))

    return nodes.filter(matchNode).map((node) => ({
        ...node,
        children: node.children ? filterByTitle(node.children, keyword) : []
    }))
}

/**
 * 필드 검색
 */
const onFieldSearch = () => {
    appliedFieldSearch.value = fieldSearchWord.value.trim()
}

/**
 * 트리 전체 펼치기
 */
const expandAllFields = () => {
    const keys = []
    const collectKeys = (nodes) => {
        nodes.forEach((node) => {
            keys.push(node.key)
            if (node.children) collectKeys(node.children)
        })
    }
    collectKeys(fieldTreeData.value)
    fieldExpandedKeys.value = keys
}

/**
 * 트리 전체 접기
 */
const collapseAllFields = () => {
    fieldExpandedKeys.value = []
}

/**
 * 필드 선택 (트리에서 클릭)
 */
const onFieldSelect = (node) => {
    // 폴더가 아닌 필드만 선택 가능
    if (node.children) return

    // 필드 상세 정보 로드
    loadFieldDetail(node.metaFieldId)
}

/**
 * 필드 트리 드래그 시작
 */
const onFieldDragStart = (info) => {
    console.log('드래그 시작:', info)
}

/**
 * 필드 트리 드롭
 */
const onFieldDrop = async (info) => {
    const dragNode = info.dragNode
    const dropNode = info.node
    const dropPosition = info.dropPosition

    console.log('=== 드롭 이벤트 ===')
    console.log('dragNode:', dragNode)
    console.log('dropNode:', dropNode)
    console.log('dropPosition:', dropPosition)

    // 드롭 가능한 위치 확인 (폴더나 테이블에만 드롭 가능)
    if (!dropNode.children && dropPosition !== 0) {
        console.warn('드롭 불가능한 위치입니다.')
        return
    }

    // 변경사항 감지
    const changes = detectTreeChanges(
        originalFieldTreeData.value,
        fieldTreeData.value
    )

    // 변경사항 저장
    await saveTreeChanges(changes)

    // 원본 데이터 업데이트
    originalFieldTreeData.value = JSON.parse(
        JSON.stringify(fieldTreeData.value)
    )
}

/**
 * fieldTreeData에 노드 추가
 * @param {string} parentNodeKey - 상위 노드의 key 값
 * @param {Object} newNode - 추가할 새 노드 객체
 * @param {boolean} isTable - 상위 노드가 테이블인 경우 true (기본값: false)
 * @returns {boolean} 성공 여부
 */
const addNodeToFieldTree = (parentNodeKey, newNode, isTable = false) => {
    if (!parentNodeKey || !newNode) {
        console.error('상위 노드 키와 새 노드는 필수입니다.')
        return false
    }

    // newNode에 필수 속성이 없으면 기본값 설정
    if (!newNode.key) {
        console.error('새 노드에는 key 속성이 필요합니다.')
        return false
    }

    if (!newNode.title) {
        newNode.title = '새 노드'
    }

    // fieldTreeData가 배열이 아니면 초기화
    if (!Array.isArray(fieldTreeData.value)) {
        fieldTreeData.value = []
    }

    // 디버깅 정보 출력
    console.log('=== addNodeToFieldTree 디버깅 ===')
    console.log('parentNodeKey:', parentNodeKey)
    console.log('isTable:', isTable)
    console.log('newNode:', newNode)
    console.log('fieldTreeData.value:', fieldTreeData.value)

    // 상위 노드가 테이블인 경우 (폴더가 아닌 경우) 최상단에 직접 추가
    if (isTable) {
        fieldTreeData.value.push({ ...newNode })
        console.log('노드가 최상단에 추가되었습니다:', newNode)
        return true
    }

    // fieldTreeData에서 parentNodeKey로 노드 찾기 (재귀)
    const findAndAddNode = (nodes, targetKey) => {
        for (let i = 0; i < nodes.length; i++) {
            const node = nodes[i]

            console.log(
                `비교 중: node.key="${node.key}" vs targetKey="${targetKey}"`
            )

            // parentNode를 찾았을 경우
            if (node.key === targetKey) {
                // children 배열이 없으면 생성
                if (!node.children) {
                    node.children = []
                }

                // 새 노드 추가
                node.children.push({ ...newNode })
                console.log(`찾음! ${targetKey}에 노드 추가됨`)
                return true
            }

            // 자식 노드에서 재귀 탐색
            if (node.children && node.children.length > 0) {
                const found = findAndAddNode(node.children, targetKey)
                if (found) return true
            }
        }
        return false
    }

    // 노드 추가 시도
    const success = findAndAddNode(fieldTreeData.value, parentNodeKey)

    if (success) {
        console.log('✓ 노드가 추가되었습니다:', newNode)
    } else {
        console.error('✗ 상위 노드를 찾을 수 없습니다. key:', parentNodeKey)
        console.error('사용 가능한 노드 키 목록:')
        const getAllKeys = (nodes, prefix = '') => {
            nodes.forEach((node) => {
                console.error(`${prefix}- ${node.key} (title: ${node.title})`)
                if (node.children && node.children.length > 0) {
                    getAllKeys(node.children, prefix + '  ')
                }
            })
        }
        getAllKeys(fieldTreeData.value)
    }

    return success
}

/**
 * fieldTreeData에서+
 *  노드 삭제
 * @param {string} nodeKey - 삭제할 노드의 key 값
 * @returns {boolean} 성공 여부
 */
const removeNodeFromFieldTree = (nodeKey) => {
    if (!nodeKey) {
        console.error('삭제할 노드 키는 필수입니다.')
        return false
    }

    // fieldTreeData가 배열이 아니면 초기화
    if (!Array.isArray(fieldTreeData.value)) {
        fieldTreeData.value = []
        return false
    }

    // 디버깅 정보 출력
    console.log('=== removeNodeFromFieldTree 디버깅 ===')
    console.log('nodeKey:', nodeKey)
    console.log('fieldTreeData.value:', fieldTreeData.value)

    // 최상위 레벨에서 노드 찾아 삭제
    const topLevelIndex = fieldTreeData.value.findIndex(
        (node) => node.key === nodeKey
    )
    if (topLevelIndex !== -1) {
        const removedNode = fieldTreeData.value.splice(topLevelIndex, 1)[0]
        console.log('✓ 최상위 노드가 삭제되었습니다:', removedNode)
        return true
    }

    // 재귀적으로 자식 노드에서 찾아 삭제
    const findAndRemoveNode = (nodes, targetKey) => {
        for (let i = 0; i < nodes.length; i++) {
            const node = nodes[i]

            // 자식 노드가 있는 경우
            if (node.children && node.children.length > 0) {
                // 자식 노드 중에서 삭제할 노드 찾기
                const childIndex = node.children.findIndex(
                    (child) => child.key === targetKey
                )

                if (childIndex !== -1) {
                    const removedNode = node.children.splice(childIndex, 1)[0]
                    console.log(
                        `✓ 노드가 삭제되었습니다 (부모: ${node.key}):`,
                        removedNode
                    )
                    return true
                }

                // 더 깊은 레벨에서 재귀 탐색
                const found = findAndRemoveNode(node.children, targetKey)
                if (found) return true
            }
        }
        return false
    }

    // 노드 삭제 시도
    const success = findAndRemoveNode(fieldTreeData.value, nodeKey)

    if (success) {
        console.log('✓ 노드 삭제 완료')
    } else {
        console.error('✗ 삭제할 노드를 찾을 수 없습니다. key:', nodeKey)
        console.error('사용 가능한 노드 키 목록:')
        const getAllKeys = (nodes, prefix = '') => {
            nodes.forEach((node) => {
                console.error(`${prefix}- ${node.key} (title: ${node.title})`)
                if (node.children && node.children.length > 0) {
                    getAllKeys(node.children, prefix + '  ')
                }
            })
        }
        getAllKeys(fieldTreeData.value)
    }

    return success
}

/**
 * fieldTreeData에서 노드 이동 (순서 변경 또는 부모 변경)
 * @param {string} nodeKey - 이동할 노드의 key 값
 * @param {string|null} newParentKey - 새로운 부모 노드의 key 값 (null이면 최상위로 이동)
 * @param {number} newOrder - 새로운 순서 (0부터 시작)
 * @returns {boolean} 성공 여부
 */
const moveNodeInFieldTree = (nodeKey, newParentKey, newOrder) => {
    if (!nodeKey) {
        console.error('이동할 노드 키는 필수입니다.')
        return false
    }

    if (!Array.isArray(fieldTreeData.value)) {
        fieldTreeData.value = []
        return false
    }

    console.log('=== moveNodeInFieldTree ===')
    console.log('nodeKey:', nodeKey)
    console.log('newParentKey:', newParentKey)
    console.log('newOrder:', newOrder)

    // 1. 노드 찾아서 제거
    let removedNode = null

    const findAndRemove = (nodes) => {
        for (let i = 0; i < nodes.length; i++) {
            const node = nodes[i]

            if (node.key === nodeKey) {
                removedNode = nodes.splice(i, 1)[0]
                return true
            }

            if (node.children && node.children.length > 0) {
                const found = findAndRemove(node.children)
                if (found) return true
            }
        }
        return false
    }

    // 최상위 레벨에서 찾기
    const topLevelIndex = fieldTreeData.value.findIndex((node) => node.key === nodeKey)
    if (topLevelIndex !== -1) {
        removedNode = fieldTreeData.value.splice(topLevelIndex, 1)[0]
    } else {
        // 하위 노드에서 찾기
        findAndRemove(fieldTreeData.value)
    }

    if (!removedNode) {
        console.error('이동할 노드를 찾을 수 없습니다:', nodeKey)
        return false
    }

    console.log('제거된 노드:', removedNode)

    // 2. 새로운 위치에 추가
    if (newParentKey === null) {
        // 최상위로 이동
        const targetIndex = Math.min(newOrder, fieldTreeData.value.length)
        fieldTreeData.value.splice(targetIndex, 0, removedNode)
        console.log(`최상위 ${targetIndex}번째 위치로 이동 완료`)
    } else {
        // 특정 부모 노드 하위로 이동
        const findAndInsert = (nodes) => {
            for (let i = 0; i < nodes.length; i++) {
                const node = nodes[i]

                if (node.key === newParentKey) {
                    if (!node.children) {
                        node.children = []
                    }
                    const targetIndex = Math.min(newOrder, node.children.length)
                    node.children.splice(targetIndex, 0, removedNode)
                    console.log(`${newParentKey}의 ${targetIndex}번째 자식으로 이동 완료`)
                    return true
                }

                if (node.children && node.children.length > 0) {
                    const found = findAndInsert(node.children)
                    if (found) return true
                }
            }
            return false
        }

        const success = findAndInsert(fieldTreeData.value)
        if (!success) {
            console.error('새로운 부모 노드를 찾을 수 없습니다:', newParentKey)
            // 원래 위치로 복구 (최상위에 추가)
            fieldTreeData.value.push(removedNode)
            return false
        }
    }

    return true
}

/**
 * fieldTreeData에 변경사항 일괄 적용
 * @param {Object} changes - { folderChanges: [], fieldChanges: [] }
 * @returns {boolean} 성공 여부
 */
const applyTreeChanges = (changes) => {
    const { folderChanges, fieldChanges } = changes

    if (!folderChanges && !fieldChanges) {
        console.error('변경사항이 없습니다.')
        return false
    }

    console.log('=== applyTreeChanges ===')
    console.log('folderChanges:', folderChanges)
    console.log('fieldChanges:', fieldChanges)

    let successCount = 0
    let failCount = 0

    // 삭제 작업 먼저 처리
    const allChanges = [...(folderChanges || []), ...(fieldChanges || [])]
    const removeChanges = allChanges.filter((c) => c.parentKey === 'remove')
    const moveChanges = allChanges.filter((c) => c.parentKey !== 'remove')

    // 1. 삭제 처리
    removeChanges.forEach((change) => {
        console.log(`삭제 처리: ${change.key}`)
        const success = removeNodeFromFieldTree(change.key)
        if (success) successCount++
        else failCount++
    })

    // 2. 이동 처리 (순서가 중요하므로 order 기준으로 정렬)
    moveChanges.sort((a, b) => a.order - b.order)

    moveChanges.forEach((change) => {
        console.log(`이동 처리: ${change.key} -> 부모: ${change.parentKey}, 순서: ${change.order}`)
        const success = moveNodeInFieldTree(change.key, change.parentKey, change.order)
        if (success) successCount++
        else failCount++
    })

    console.log(`처리 결과: 성공 ${successCount}, 실패 ${failCount}`)

    return failCount === 0
}

/**
 * 드래그 이동으로 인한 변경사항 감지 및 저장
 * @param {Array} originalTreeData - 원본 트리 데이터 (변경 전)
 * @param {Array} currentTreeData - 현재 트리 데이터 (변경 후)
 * @returns {Object} { folderChanges: [], fieldChanges: [] }
 */
const detectTreeChanges = (originalTreeData, currentTreeData) => {
    const folderChanges = [] // 폴더 변경사항
    const fieldChanges = [] // 필드 변경사항

    // 원본 데이터를 평탄화하여 맵으로 저장 (key -> {parentKey, order})
    const originalMap = new Map()
    const flattenOriginal = (nodes, parentKey = null, level = 0) => {
        nodes.forEach((node, index) => {
            originalMap.set(node.key, {
                parentKey: parentKey,
                order: index,
                level: level
            })
            if (node.children && node.children.length > 0) {
                flattenOriginal(node.children, node.key, level + 1)
            }
        })
    }
    flattenOriginal(originalTreeData)

    // 현재 데이터를 순회하며 변경사항 감지
    const detectChanges = (nodes, parentKey = null, level = 0) => {
        nodes.forEach((node, index) => {
            const original = originalMap.get(node.key)

            if (original) {
                // 부모키 또는 순서가 변경되었는지 확인
                const parentChanged = original.parentKey !== parentKey
                const orderChanged = original.order !== index

                if (parentChanged || orderChanged) {
                    // 폴더인지 필드인지 구분 (children이 있거나 key가 'MR', 'folder'로 시작하면 폴더)
                    const isFolder =
                        node.children !== undefined ||
                        node.key.startsWith('MR') ||
                        node.key.startsWith('folder')

                    const changeData = {
                        key: node.key,
                        parentKey: parentKey,
                        order: index,
                        originalParentKey: original.parentKey,
                        originalOrder: original.order
                    }

                    if (isFolder) {
                        folderChanges.push(changeData)
                    } else {
                        fieldChanges.push(changeData)
                    }

                    console.log(
                        `변경 감지 - ${isFolder ? '폴더' : '필드'}: ${
                            node.key
                        }`,
                        changeData
                    )
                }

                // 원본 맵에서 제거 (나중에 삭제된 항목 확인용)
                originalMap.delete(node.key)
            }

            // 자식 노드 재귀 처리
            if (node.children && node.children.length > 0) {
                detectChanges(node.children, node.key, level + 1)
            }
        })
    }
    detectChanges(currentTreeData)

    // 남아있는 항목들은 삭제된 항목
    originalMap.forEach((value, key) => {
        const isFolder = key.startsWith('MR') || key.startsWith('folder')

        const removeData = {
            key: key,
            parentKey: 'remove',
            order: -1,
            originalParentKey: value.parentKey,
            originalOrder: value.order
        }

        if (isFolder) {
            folderChanges.push(removeData)
        } else {
            fieldChanges.push(removeData)
        }

        console.log(`삭제 감지 - ${isFolder ? '폴더' : '필드'}: ${key}`)
    })

    console.log('=== 변경사항 감지 결과 ===')
    console.log('폴더 변경:', folderChanges)
    console.log('필드 변경:', fieldChanges)

    return { folderChanges, fieldChanges }
}

/**
 * 트리 변경사항을 서버에 저장
 * @param {Object} changes - { folderChanges: [], fieldChanges: [] }
 */
const saveTreeChanges = async (changes) => {
    const { folderChanges, fieldChanges } = changes

    // 변경사항이 없으면 리턴
    if (folderChanges.length === 0 && fieldChanges.length === 0) {
        console.log('변경사항이 없습니다.')
        return
    }

    try {
        // 폴더 변경사항을 API 형식에 맞게 변환
        const metaTreeModelList = folderChanges.map((change) => ({
            metaTreeId: change.key,
            upMetaTreeId:
                change.parentKey === 'remove' ? null : change.parentKey,
            metaTreeOrder: change.order,
            action: change.parentKey === 'remove' ? 'remove' : 'update'
        }))

        // 필드 변경사항을 API 형식에 맞게 변환
        const metaFieldModelList = fieldChanges.map((change) => ({
            metaFieldId: change.key,
            metaTreeId: change.parentKey === 'remove' ? null : change.parentKey,
            metaFieldOrder: change.order,
            action: change.parentKey === 'remove' ? 'remove' : 'update'
        }))

        console.log('=== 서버 전송 데이터 ===')
        console.log('metaTreeModelList:', metaTreeModelList)
        console.log('metaFieldModelList:', metaFieldModelList)

        // TODO: API 호출
        // await instance.post('/api/admin/meta/updateJsTreeItem', {
        //     metaFieldModelList,
        //     metaTreeModelList
        // })

        alert('변경사항이 저장되었습니다.')

        // 트리 새로고침
        await loadFieldTree()
    } catch (error) {
        console.error('트리 변경사항 저장 오류:', error)
        alert('변경사항 저장에 실패했습니다.')
    }
}

/**
 * 폴더 추가
 */
const insertMetaTree = async (parentNodeKey) => {
    try {
        const metaTableId = selectedTableId.value

        // TODO: API 호출
        // await instance.post('/api/admin/meta/insertMetaTree', {
        //     metaTableId,
        //     upMetaTreeId: parentNodeKey === metaTableId ? null : parentNodeKey,
        //     metaTreeName: '새 폴더',
        //     metaTreeOrder: 1 // 계산 필요
        // })

        console.log('폴더 추가:', { parentNodeKey })

        // 트리 새로고침
        await loadFieldTree()
        alert('폴더가 추가되었습니다.')
    } catch (error) {
        console.error('폴더 추가 오류:', error)
        alert('폴더 추가에 실패했습니다.')
    }
}

/**
 * 폴더 이름 변경
 */
const renameMetaTree = async (nodeKey, newName) => {
    try {
        // TODO: API 호출
        // await instance.post('/api/admin/meta/renameMetaTree', {
        //     metaTreeId: nodeKey,
        //     metaTreeName: newName
        // })

        console.log('폴더 이름 변경:', { nodeKey, newName })

        // 트리 새로고침
        await loadFieldTree()
        alert('폴더 이름이 변경되었습니다.')
    } catch (error) {
        console.error('폴더 이름 변경 오류:', error)
        alert('폴더 이름 변경에 실패했습니다.')
    }
}

/**
 * 폴더 삭제
 */
const deleteMetaTree = async (nodeKey) => {
    if (!confirm('폴더를 삭제하시겠습니까?')) {
        return
    }

    try {
        // TODO: API 호출
        // const response = await instance.post('/api/admin/meta/deleteMetaTree', {
        //     metaTreeId: nodeKey
        // })

        // if (response.data.returnCode === 'E001') {
        //     alert(response.data.returnMessage)
        //     return
        // }

        console.log('폴더 삭제:', { nodeKey })

        // 트리 새로고침
        await loadFieldTree()
        alert('폴더가 삭제되었습니다.')
    } catch (error) {
        console.error('폴더 삭제 오류:', error)
        alert('폴더 삭제에 실패했습니다.')
    }
}

/**
 * 필드 상세 정보 로드
 */
const loadFieldDetail = async (fieldId) => {
    try {
        // TODO: API 호출
        // const response = await instance.get(`/api/admin/meta/field/${fieldId}`)
        // Object.assign(metaFieldForm, response.data)

        // 임시 데이터
        Object.assign(metaFieldForm, {
            metaFieldId: fieldId,
            activeYn: 'Y',
            dataType: 'string',
            metaField: 'customer_name',
            metaFieldName: '고객명',
            maskYn: false,
            maskType: '',
            infoSecurYn: false,
            dimensionYn: false,
            bidwDimensionYn: false,
            dimensionCretDay: '',
            dimensionDay: '',
            comment: '고객 이름',
            imgPath: '',
            requiredYn: true,
            easyConditionYn: true,
            easyItemYn: true,
            easyCatalogue: '기본정보',
            regDate: '2025-01-01 10:00:00',
            changDate: '2025-01-15 14:30:00',
            regId: 'admin',
            changId: 'admin'
        })

        hasMetaFieldChange.value = false
    } catch (error) {
        console.error('필드 상세 조회 오류:', error)
    }
}

/**
 * 메타 테이블 정보 변경
 */
const onMetaTableChange = () => {
    hasMetaTableChange.value = true
}

/**
 * 메타 테이블 저장
 */
const updateMetaTable = async () => {
    if (!hasMetaTableChange.value) {
        alert('변경된 내용이 없습니다.')
        return
    }

    try {
        // TODO: API 호출
        // await instance.put('/api/admin/meta/table', metaTableForm)

        console.log('메타 테이블 저장:', metaTableForm)
        alert('저장되었습니다.')
        hasMetaTableChange.value = false
    } catch (error) {
        console.error('메타 테이블 저장 오류:', error)
        alert('저장에 실패했습니다.')
    }
}

/**
 * 메타 필드 정보 변경
 */
const onMetaFieldChange = () => {
    hasMetaFieldChange.value = true
}

/**
 * 관점 여부 변경 (dimensionYn과 bidwDimensionYn은 동시에 Y 불가능)
 */
const onDimensionChange = (event) => {
    const targetId = event.target.id
    if (
        targetId === 'admin_meta_field_form_meta_dimension_yn' &&
        metaFieldForm.dimensionYn
    ) {
        metaFieldForm.bidwDimensionYn = false
    } else if (
        targetId === 'admin_meta_field_form_bidw_meta_dimension_yn' &&
        metaFieldForm.bidwDimensionYn
    ) {
        metaFieldForm.dimensionYn = false
    }
    hasMetaFieldChange.value = true
}

/**
 * 필드 이미지 업로드
 */
const handleFieldImageUpload = async (event) => {
    const file = event.target.files?.[0]
    if (file) {
        metaFieldForm.imgPath = `${file.name} (${file.size} bytes)`

        // 파일 업로드 처리
        const metaFieldId = metaFieldForm.metaFieldId
        await insertMetaInfo('field', metaFieldId, file)

        event.target.value = '' // input 초기화
    }
}

/**
 * 테이블 이미지 업로드
 */
const handleTableImageUpload = async (event) => {
    const file = event.target.files?.[0]
    if (file) {
        metaTableForm.imgPath = `${file.name} (${file.size} bytes)`

        // 파일 업로드 처리
        const metaTableId = metaTableForm.metaTableId
        await insertMetaInfo('table', metaTableId, file)

        event.target.value = '' // input 초기화
    }
}

/**
 * 메타 정보 이미지 업로드 (테이블 또는 필드)
 */
const insertMetaInfo = async (metaInfoType, metaInfoId, file) => {
    try {
        const metaInfoImgPath = `${metaInfoId}.png`

        // 1. 메타 정보 업데이트 (이미지 경로 저장)
        // TODO: API 호출
        // await instance.post('/api/admin/meta/updateMetaInfo', {
        //     metaInfoId,
        //     metaInfoType,
        //     metaInfoImgPath
        // })

        console.log('메타 정보 업데이트:', {
            metaInfoId,
            metaInfoType,
            metaInfoImgPath
        })

        // 2. 파일 업로드
        await uploadMetaInfoImg(metaInfoType, file)

        // 3. 목록 새로고침
        if (metaInfoType === 'table') {
            await selectMetaTableList()
        } else if (metaInfoType === 'field') {
            await loadFieldTree()
        }

        alert('이미지 업로드가 완료되었습니다.')
    } catch (error) {
        console.error('메타 정보 이미지 업로드 오류:', error)
        alert('이미지 업로드에 실패했습니다.')
    }
}

/**
 * 메타 정보 이미지 파일 업로드
 */
const uploadMetaInfoImg = async (metaInfoType, file) => {
    try {
        const formData = new FormData()
        formData.append('meta_info_img_upload', file)

        // TODO: API 호출
        // await instance.post('/api/admin/meta/uploadMetaInfoImg', formData, {
        //     headers: {
        //         'Content-Type': 'multipart/form-data'
        //     }
        // })

        console.log('파일 업로드:', file)
    } catch (error) {
        console.error('파일 업로드 오류:', error)
        throw error
    }
}

/**
 * 메타 필드 저장
 */
const updateMetaField = async () => {
    if (!hasMetaFieldChange.value) {
        alert('변경된 내용이 없습니다.')
        return
    }

    try {
        // TODO: API 호출
        // await instance.put('/api/admin/meta/field', metaFieldForm)

        console.log('메타 필드 저장:', metaFieldForm)
        alert('저장되었습니다.')
        hasMetaFieldChange.value = false
    } catch (error) {
        console.error('메타 필드 저장 오류:', error)
        alert('저장에 실패했습니다.')
    }
}

/**
 * 관점 생성 요청
 */
const selectDimensionList = () => {
    showDimensionListModal.value = true
}

/**
 * 관점 생성 결과
 */
const showDimensionQueueResult = () => {
    showDimensionQueueResultModal.value = true
}

/**
 * 테이블 복제 모달
 */
const showCopyMetaTableModal = () => {
    showCopyTableModal.value = true
}

/**
 * 테이블 삭제 모달
 */
const showDropMetaTableModal = () => {
    showDropTableModal.value = true
}

/**
 * 필드 추가 모달
 */
const showAddMetaFieldModal = () => {
    showAddFieldModal.value = true
}

/**
 * 필드 속성 일괄 변경 모달
 */
const showEditMetaFieldInfoModal = () => {
    showEditFieldInfoModal.value = true
}

// ===== 모달 이벤트 핸들러 =====

/**
 * 관점 저장
 */
const onDimensionSave = (payload) => {
    console.log('관점 저장:', payload)
    // TODO: 트리 새로고침
}

/**
 * 테이블 복제
 */
const onTableCopy = (payload) => {
    console.log('테이블 복제:', payload)
    selectMetaTableList()
}

/**
 * 테이블 삭제
 */
const onTableDelete = (tableId) => {
    console.log('테이블 삭제:', tableId)
    selectedTableId.value = null
    selectMetaTableList()
}

/**
 * 필드 추가
 */
const onFieldAdd = (payload) => {
    console.log('필드 추가:', payload)
    loadFieldTree()
}

/**
 * 필드 일괄 업데이트
 */
const onFieldBatchUpdate = (fields) => {
    console.log('필드 일괄 업데이트:', fields)
    loadFieldTree()
}

/**
 * 관점 생성 결과 검색 조건 초기화
 */
const initDimensionResultSearchInput = () => {
    // TODO: 관점 생성 결과 모달의 검색 조건 초기화
    console.log('관점 생성 결과 검색 조건 초기화')
}

/**
 * 복제 테이블 버튼 토글 (사용 중단)
 * 테이블삭제 Batch 개발로 인하여 사용중단 2023-09-07
 */
const toggleCopyDeleteBtn = () => {
    const metaTableId = metaTableForm.metaTableId
    if (metaTableId.indexOf('VT') > -1) {
        showDeleteBtn.value = true
    } else {
        showDeleteBtn.value = false
    }
}

/**
 * 관점 생성 상태 업데이트
 */
const updateDimensionQueueStatus = async (dimensionQueueId) => {
    try {
        // TODO: API 호출
        // await instance.post('/api/admin/meta/updateDimensionQueueStatus', {
        //     dimensionQueueId
        // })

        console.log('관점 생성 상태 업데이트:', dimensionQueueId)
    } catch (error) {
        console.error('관점 생성 상태 업데이트 오류:', error)
    }
}

/**
 * 에러 메시지 클립보드 복사
 */
const copyProgressComment = (text) => {
    if (!text || text === 'undefined' || text === 'null') {
        return
    }

    // 클립보드 API 사용
    if (navigator.clipboard && window.isSecureContext) {
        navigator.clipboard
            .writeText(text)
            .then(() => {
                alert('클립보드에 복사되었습니다.')
            })
            .catch((err) => {
                console.error('클립보드 복사 실패:', err)
            })
    } else {
        // 구버전 브라우저 대응
        const textArea = document.createElement('textarea')
        textArea.value = text
        textArea.style.position = 'fixed'
        textArea.style.left = '-999999px'
        document.body.appendChild(textArea)
        textArea.focus()
        textArea.select()

        try {
            const successful = document.execCommand('copy')
            if (successful) {
                alert('클립보드에 복사되었습니다.')
            }
        } catch (err) {
            console.error('클립보드 복사 실패:', err)
        }

        document.body.removeChild(textArea)
    }
}

/**
 * HTML 특수문자 이스케이프
 */
const escapeHtml = (text) => {
    if (!text) return ''
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    }
    return text.replace(/[&<>"']/g, (m) => map[m])
}

/**
 * 관점 생성 상태 HTML 반환
 */
const innerStatusHtml = (status, progressComment) => {
    const escapedComment = escapeHtml(progressComment)

    switch (status) {
        case 'r':
            return `<span class="badge badge-light-warning" title="${escapedComment}">작업대기중</span>`
        case 'p':
            return `<span class="badge badge-light-warning" title="${escapedComment}">작업진행중</span>`
        case 'c':
            return `<span class="badge badge-light-danger" title="${escapedComment}">작업취소</span>`
        case 's':
            return `<span class="badge badge-light-success" title="${escapedComment}">작업완료</span>`
        case 'e':
            return `<a href="javascript:void(0)" @click="copyProgressComment('${escapedComment}')"><span class="badge badge-light-dark" title="${escapedComment}">시스템오류</span></a>`
        default:
            return ''
    }
}

/**
 * 테이블 삭제 상세 정보 토글
 */
const toggleDropTableDetail = (type) => {
    // TODO: 테이블 삭제 모달 내부 상세 정보 토글
    console.log('테이블 삭제 상세 정보 토글:', type)
}

/**
 * 복제 테이블 확인 삭제 (사용 중단)
 * 테이블삭제 Batch 개발로 인하여 사용중단 2023-09-07
 */
const confirmDeleteCopyTable = () => {
    const metaTableId = selectedTableId.value
    const metaTableName = metaTableForm.metaTableName
    const msg = `복제 테이블 '[복제] ${metaTableName}'을(를) 정말 삭제 하시겠습니까?`

    if (confirm(msg)) {
        deleteCopyTableProc(metaTableId)
    }
}

/**
 * 복제 테이블 삭제 처리 (사용 중단)
 * 테이블삭제 Batch 개발로 인하여 사용중단 2023-09-07
 */
const deleteCopyTableProc = async (metaTableId) => {
    if (metaTableId.indexOf('MT') > -1) {
        alert(
            `복제 테이블만 삭제 가능합니다.\n대상 테이블 아이디: ${metaTableId}`
        )
        return
    }

    try {
        // TODO: API 호출
        // const response = await instance.post('/api/admin/meta/deleteCopyTableProc', {
        //     metaTableId
        // })

        console.log('복제 테이블 삭제:', metaTableId)
        alert('정상적으로 삭제되었습니다.')

        // 첫 번째 테이블 선택
        selectedTableId.value = null
        await selectMetaTableList()
    } catch (error) {
        console.error('복제 테이블 삭제 오류:', error)
        alert('삭제에 실패했습니다.')
    }
}

// ===== Lifecycle =====
onMounted(() => {
    selectMetaTableList()
})

// ===== 내보내기 (사용하지 않는 함수들을 추후 연결을 위해 주석 처리) =====
// 다음 함수들은 템플릿에서 직접 사용되지 않지만, 추후 기능 확장을 위해 정의됨:
// - onFieldDragStart, onFieldDrop, updateJsTreeItem
// - insertMetaTree, renameMetaTree, deleteMetaTree
// - handleTableImageUpload, uploadMetaInfoImg
// - toggleCopyDeleteBtn, confirmDeleteCopyTable, deleteCopyTableProc
// - updateDimensionQueueStatus, copyProgressComment, innerStatusHtml
// - toggleDropTableDetail, initDimensionResultSearchInput
</script>

<style scoped>
.cursor-pointer {
    cursor: pointer;
}

.ta-right {
    text-align: right;
}

.toastr {
    display: inline-block;
    padding: 0.85rem 1.25rem;
    border-radius: 0.475rem;
    background-color: #f1416c;
    color: white;
}

.toastr-message {
    font-size: 0.925rem;
}

.toastr-position-meta-table {
    position: absolute;
    right: 0;
    top: -60px;
}

.toastr-position-meta-field {
    position: absolute;
    right: 0;
    top: -60px;
}

.z-index-3 {
    z-index: 3;
}
</style>
