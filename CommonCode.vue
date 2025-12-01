<template>
    <PageHeader
        title="공통코드 관리"
        parent="시스템관리"
        grandParent="관리자"
    />

    <div class="admin-wrapper common-code-wrapper">
        <!-- 좌측: 그룹코드 / 상위코드 목록 -->
        <div class="admin-sidebar">
            <b-card
                header-class="admin-sidebar-header"
                footer-class="admin-sidebar-footer"
            >
                <!-- ⭐ Velzon 탭 -->
                <template #header>
                    <ul
                        class="nav nav-tabs-custom card-header-tabs nav-justified border-bottom-0"
                    >
                        <li class="nav-item">
                            <a
                                href="javascript:void(0);"
                                class="nav-link"
                                :class="{ active: activeTab === 'group' }"
                                @click="activeTab = 'group'"
                                >그룹코드 목록</a
                            >
                        </li>

                        <li class="nav-item">
                            <a
                                href="javascript:void(0);"
                                class="nav-link"
                                :class="{ active: activeTab === 'upper' }"
                                @click="activeTab = 'upper'"
                                >상위코드 목록</a
                            >
                        </li>
                    </ul>
                </template>

                <!-- -----------------------------
                    좌측 탭 컨텐츠
                ------------------------------ -->
                <div class="tab-content">
                    <!-- ★ 그룹코드 탭 -->
                    <div
                        class="tab-pane fade"
                        :class="{ 'show active': activeTab === 'group' }"
                    >
                        <!-- 공통 검색 UI -->
                        <div
                            class="form-search-wrap w-auto mb-2 position-relative"
                        >
                            <input
                                type="text"
                                v-model="searchKeyword"
                                class="form-control"
                                placeholder="그룹코드를 입력하세요"
                                autocomplete="off"
                            />
                            <b-button
                                variant="link"
                                class="btn-icon search-widget-icon"
                            >
                                <i class="ti ti-search"></i>
                            </b-button>
                        </div>

                        <!-- 목록 영역 -->
                        <Simplebar
                            :style="{ maxHeight: leftHeight + 'px' }"
                            class="group-code-list"
                        >
                            <b-list-group tag="ol" class="list-group-numbered">
                                <b-list-group-item
                                    tag="li"
                                    v-for="(group, i) in filteredGroups"
                                    :key="i"
                                    class="list-group-item-action hstack"
                                    :class="{
                                        active: selectedGroup === group.code
                                    }"
                                    @click="selectGroup(group)"
                                >
                                    <span>{{ group.code }}</span>
                                    <b-badge
                                        variant="primary-subtle text-dark"
                                        pill
                                        class="ms-auto"
                                    >
                                        {{ group.count }}
                                    </b-badge>
                                </b-list-group-item>
                            </b-list-group>
                        </Simplebar>
                    </div>

                    <!-- ★ 상위코드 탭 -->
                    <div
                        class="tab-pane fade"
                        :class="{ 'show active': activeTab === 'upper' }"
                    >
                        <!-- 동일한 검색 UI -->
                        <div
                            class="form-search-wrap w-auto mb-2 position-relative"
                        >
                            <input
                                type="text"
                                v-model="searchKeywordUpper"
                                class="form-control"
                                placeholder="상위코드를 입력하세요"
                                autocomplete="off"
                            />
                            <b-button
                                variant="link"
                                class="btn-icon search-widget-icon"
                            >
                                <i class="ti ti-search"></i>
                            </b-button>
                        </div>

                        <!-- 상위코드 리스트 (샘플) -->
                        <Simplebar
                            :style="{ maxHeight: leftHeight + 'px' }"
                            class="group-code-list"
                        >
                            <b-list-group>
                                <b-list-group-item
                                    v-for="u in filteredUppers"
                                    :key="u.code"
                                    class="list-group-item-action hstack"
                                    :class="{
                                        active: selectedUpper === u.code
                                    }"
                                    @click="selectUpper(u)"
                                >
                                    <span>{{ u.code }}</span>
                                    <b-badge pill class="ms-auto">{{
                                        u.count
                                    }}</b-badge>
                                </b-list-group-item>
                            </b-list-group>
                        </Simplebar>
                    </div>
                </div>

                <!-- 기존 footer(신규 그룹코드 추가 UI)는 그대로 유지 -->
                <template #footer>
                    <div class="add-list-box" v-if="isAddingGroup">
                        <h4 class="mb-0">그룹코드 추가</h4>
                        <b-form-input
                            v-model="newGroupCode"
                            placeholder="그룹코드를 입력하세요"
                        />
                        <div class="btn-area">
                            <b-button variant="light" @click="cancelAddGroup"
                                >취소</b-button
                            >
                            <b-button variant="dark" @click="confirmAddGroup"
                                >저장</b-button
                            >
                        </div>
                    </div>
                </template>
            </b-card>
        </div>

        <!-- ============================
            우측: 공통코드 상세 목록
        ============================ -->
        <!-- ---------------------------
      우측: 공통코드 상세
---------------------------- -->
        <div class="admin-content">
            <b-card header-class="d-flex align-items-center">
                <template #header>
                    <h4 class="card-title mb-0">
                        <template v-if="selectedKey">
                            <span class="text-primary fw-semibold">
                                [{{ selectedKey }}]
                            </span>
                            <span class="ms-1 text-dark">
                                {{
                                    activeTab === 'group'
                                        ? '공통코드'
                                        : '상위코드'
                                }}
                                목록
                            </span>
                        </template>

                        <template v-else>
                            <span class="text-muted fw-normal">
                                <i class="ti ti-info-circle align-middle"></i>
                                선택된 코드가 없습니다.
                            </span>
                        </template>
                    </h4>

                    <!-- ⭐ 버튼 4종 (선택된 코드 있을 때만 표시) -->
                    <div v-if="selectedKey" class="hstack gap-2 ms-auto">
                        <b-button variant="light-2" @click="addNewRow">
                            <i class="ti ti-plus"></i> 추가
                        </b-button>

                        <div class="vr m-1"></div>

                        <b-button variant="soft-danger" @click="deleteSelected">
                            <i class="ti ti-trash"></i> 삭제
                        </b-button>

                        <b-button variant="soft-primary" @click="saveRows">
                            <i class="ti ti-device-floppy"></i> 저장
                        </b-button>

                        <b-button variant="light" @click="cancelEdit">
                            <i class="ti ti-x"></i> 취소
                        </b-button>
                    </div>
                </template>

                <!-- 테이블 영역 -->
                <Simplebar
                    :style="{ height: rightHeight + 'px' }"
                    class="common-code-list"
                >
                    <table class="table table-sm align-middle text-center">
                        <thead class="table-light">
                            <tr>
                                <th style="width: 30px">
                                    <b-form-checkbox
                                        v-model="selectAll"
                                        @change="toggleSelectAll"
                                        class="form-check"
                                    />
                                </th>
                                <th>
                                    {{
                                        activeTab === 'group'
                                            ? '공통코드'
                                            : '상위코드'
                                    }}
                                </th>
                                <th>
                                    {{
                                        activeTab === 'group'
                                            ? '공통코드명'
                                            : '상위코드명'
                                    }}
                                </th>
                                <th>코드값</th>
                                <th style="width: 60px">정렬순서</th>
                                <th>
                                    {{
                                        activeTab === 'group'
                                            ? '공통코드ID'
                                            : '상위코드ID'
                                    }}
                                </th>
                                <th>등록일시</th>
                                <th>변경일시</th>
                                <th>생성자</th>
                                <th>수정자</th>
                            </tr>
                        </thead>

                        <tbody>
                            <!-- 행 반복 -->
                            <tr v-for="(item, i) in pagedCodes" :key="item.id">
                                <!-- 체크박스 -->
                                <td>
                                    <b-form-checkbox
                                        class="form-check"
                                        v-model="selectedIds"
                                        :value="item.id"
                                    />
                                </td>

                                <!-- 편집 가능한 컬럼들 -->
                                <td>
                                    <b-form-input
                                        v-model="item.code"
                                        @input="markEdited(item)"
                                    />
                                </td>

                                <td>
                                    <b-form-input
                                        v-model="item.name"
                                        @input="markEdited(item)"
                                    />
                                </td>

                                <td>
                                    <b-form-input
                                        v-model="item.value"
                                        @input="markEdited(item)"
                                    />
                                </td>

                                <td>
                                    <b-form-input
                                        type="number"
                                        v-model="item.sortOrder"
                                        class="text-end"
                                        @input="markEdited(item)"
                                    />
                                </td>

                                <!-- readonly 영역 -->
                                <td class="text-start">{{ item.id }}</td>
                                <td>{{ item.createdAt }}</td>
                                <td>{{ item.updatedAt }}</td>
                                <td>{{ item.creator }}</td>
                                <td>{{ item.modifier }}</td>
                            </tr>

                            <!-- No data -->
                            <tr v-if="pagedCodes.length === 0">
                                <td colspan="10">
                                    <EmptyMessage>
                                        선택된 코드의 데이터가 없습니다.
                                    </EmptyMessage>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </Simplebar>

                <Pager
                    :page="page"
                    :total="totalPages"
                    @update:page="page = $event"
                />
            </b-card>
        </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import Simplebar from 'simplebar-vue'
import PageHeader from '@/components/PageHeader'
import Pager from '@/components/Pager.vue'
import EmptyMessage from '@/components/EmptyMessage.vue'

/* -------------------------------  
   좌측 탭 상태
--------------------------------*/
const activeTab = ref('group') // group | upper

/* -------------------------------
   검색 키워드
--------------------------------*/
const searchKeyword = ref('')
const searchKeywordUpper = ref('')

/* ------------------------------------
 * 그룹코드 / 상위코드 목록 (샘플)
 * ------------------------------------ */
const groupCodes = ref([
    { code: 'SYS001', name: '시스템 설정', count: 4 },
    { code: 'USER001', name: '사용자 상태', count: 6 }
])

const upperCodes = ref([
    { code: 'UP100', name: '상위코드-공통', count: 3 },
    { code: 'UP200', name: '상위코드-설정', count: 5 }
])

/* 검색 필터 */
const filteredGroups = computed(() =>
    groupCodes.value.filter(
        (g) =>
            g.code.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
            g.name.includes(searchKeyword.value)
    )
)

const filteredUppers = computed(() =>
    upperCodes.value.filter(
        (u) =>
            u.code
                .toLowerCase()
                .includes(searchKeywordUpper.value.toLowerCase()) ||
            u.name.includes(searchKeywordUpper.value)
    )
)

/* ------------------------------------
 * 선택된 코드
 * ------------------------------------ */
const selectedGroup = ref(null)
const selectedUpper = ref(null)

const selectedKey = computed(() =>
    activeTab.value === 'group'
        ? selectedGroup.value?.code
        : selectedUpper.value?.code
)

/* ------------------------------------
 * 우측 테이블 데이터
 * ------------------------------------ */
const codeList = ref([])

/* 페이지네이션 */
const page = ref(1)
const pageSize = 10
const totalPages = computed(() => Math.ceil(codeList.value.length / pageSize))

const pagedCodes = computed(() => {
    const start = (page.value - 1) * pageSize
    return codeList.value.slice(start, start + pageSize)
})

/* ------------------------------------
 * Simplebar 자동 높이 계산
 * ------------------------------------ */
const rightHeight = ref(400)
const leftHeight = ref(400)

function updateHeights() {
    const headerH = 56
    const pageHeaderH = 94
    const padding = 98

    const totalOffset = headerH + pageHeaderH + padding

    rightHeight.value = window.innerHeight - totalOffset
    leftHeight.value = window.innerHeight - totalOffset
}

onMounted(() => {
    updateHeights()
    window.addEventListener('resize', updateHeights)
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', updateHeights)
})

/* ------------------------------------
 * 샘플데이터 로드
 * ------------------------------------ */
function loadSampleData(key) {
    if (!key) {
        codeList.value = []
        return
    }

    codeList.value = Array.from({ length: 5 }, (_, i) => ({
        id: `${key}-${i + 1}`,
        code: `${key}_CODE${i + 1}`,
        name: `${activeTab.value === 'group' ? '공통코드명' : '상위코드명'} ${
            i + 1
        }`,
        value: `VAL${i + 1}`,
        sortOrder: i + 1,
        createdAt: '2025-11-25',
        updatedAt: '2025-11-25',
        creator: 'admin',
        modifier: 'manager',
        _edited: false
    }))
}

/* ------------------------------------
 * 좌측 리스트 선택
 * ------------------------------------ */
function selectGroup(item) {
    selectedGroup.value = item
    selectedUpper.value = null
    activeTab.value = 'group'
    loadSampleData(item.code)
}

function selectUpper(item) {
    selectedUpper.value = item
    selectedGroup.value = null
    activeTab.value = 'upper'
    loadSampleData(item.code)
}

/* ------------------------------------
 * 편집 / 체크박스
 * ------------------------------------ */
const selectedIds = ref([])
const selectAll = ref(false)

function toggleSelectAll() {
    if (selectAll.value) {
        selectedIds.value = pagedCodes.value.map((row) => row.id)
    } else {
        selectedIds.value = []
    }
}

/* ⭐ 수정 시 자동 체크 기능 다시 복구 */
function markEdited(item) {
    item._edited = true

    // 체크박스 자동 선택
    if (!selectedIds.value.includes(item.id)) {
        selectedIds.value.push(item.id)
    }
}

/* ------------------------------------
 * 행 추가
 * ------------------------------------ */
function addNewRow() {
    if (!selectedKey.value) {
        alert('코드를 먼저 선택하세요.')
        return
    }

    const newId = `${selectedKey.value}-${Date.now()}`

    codeList.value.push({
        id: newId,
        code: '',
        name: '',
        value: '',
        sortOrder: codeList.value.length + 1,
        createdAt: new Date().toISOString().slice(0, 10),
        updatedAt: '',
        creator: 'admin',
        modifier: '',
        _edited: true
    })

    // count 업데이트
    if (activeTab.value === 'group') {
        const item = groupCodes.value.find((v) => v.code === selectedKey.value)
        if (item) item.count = codeList.value.length
    } else {
        const item = upperCodes.value.find((v) => v.code === selectedKey.value)
        if (item) item.count = codeList.value.length
    }
}

/* ------------------------------------
 * 삭제
 * ------------------------------------ */
function deleteSelected() {
    if (selectedIds.value.length === 0) {
        alert('삭제할 항목을 선택하세요.')
        return
    }

    codeList.value = codeList.value.filter(
        (row) => !selectedIds.value.includes(row.id)
    )

    selectedIds.value = []
    selectAll.value = false
}

/* ------------------------------------
 * 저장
 * ------------------------------------ */
function saveRows() {
    codeList.value.forEach((item) => {
        if (item._edited) {
            item.updatedAt = new Date().toISOString().slice(0, 10)
            item.modifier = 'admin'
            item._edited = false
        }
    })
    alert('저장되었습니다.')
}

/* ------------------------------------
 * 취소
 * ------------------------------------ */
function cancelEdit() {
    loadSampleData(selectedKey.value)
    selectedIds.value = []
    selectAll.value = false
}

/* ------------------------------------
 * 탭 변경 시 정리
 * ------------------------------------ */
watch(activeTab, () => {
    page.value = 1
    selectedIds.value = []
    selectAll.value = false
    codeList.value = []

    if (activeTab.value === 'group' && selectedGroup.value) {
        loadSampleData(selectedGroup.value.code)
    }
    if (activeTab.value === 'upper' && selectedUpper.value) {
        loadSampleData(selectedUpper.value.code)
    }
})
</script>
