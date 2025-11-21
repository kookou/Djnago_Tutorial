<template>
    <b-modal
        v-model="show"
        title="워크북 경로 저장"
        centered
        scrollable
        size="md"
        hide-header-close
        class="workbook-path-save"
        v-show="isSaveModalVisible"
    >
        <!-- 탭 -->
        <b-tabs
            v-model="activeTab"
            pills
            justified
            nav-class="custom-hover-nav-tabs"
        >
            <b-tab title="내 워크북" :value="0">
                <Simplebar>
                    <b-list-group class="path-list list-group-flush">
                        <b-list-group-item
                            v-for="workbook in myWorkbookPaths"
                            :key="workbook.targetWorkbookId"
                            class="hstack gap-1 list-group-item-action"
                            :class="{
                                active:
                                    selectedWorkbook?.targetWorkbookId ===
                                    workbook.targetWorkbookId
                            }"
                            @click="selectedWorkbook = workbook"
                        >
                            <i
                                class="ti ti-folder-filled fs-16 text-primary opacity-50"
                            ></i>
                            <span>{{ workbook.targetWorkbookName }}</span>
                        </b-list-group-item>
                    </b-list-group>
                </Simplebar>
            </b-tab>

            <b-tab title="공용 워크북" :value="1">
                <Simplebar>
                    <b-list-group class="path-list list-group-flush">
                        <b-list-group-item
                            v-for="workbook in commonWorkbookPaths"
                            :key="workbook.targetWorkbookId"
                            class="hstack gap-1 list-group-item-action"
                            :class="{
                                active:
                                    selectedWorkbook?.targetWorkbookId ===
                                    workbook.targetWorkbookId
                            }"
                            @click="selectedWorkbook = workbook"
                        >
                            <i
                                class="ti ti-folder-filled fs-16 text-primary opacity-50"
                            ></i>
                            <span>{{ workbook.targetWorkbookName }}</span>
                        </b-list-group-item>
                    </b-list-group>
                </Simplebar>
            </b-tab>
        </b-tabs>

        <!-- 타겟 작업명 입력 -->
        <div class="mt-3 pt-3 border-top border-top-dashed">
            <div class="d-flex justify-content-between align-items-center mb-1">
                <label class="form-label mb-0">타겟 작업명 입력</label>
                <small
                    :class="[
                        'text-muted',
                        { 'text-danger fw-semibold': targetName.length > 50 }
                    ]"
                >
                    {{ targetName.length }}/50
                </small>
            </div>

            <b-form-input
                v-model="targetName"
                placeholder="저장할 타겟 작업명을 입력하세요"
                :maxlength="50"
            ></b-form-input>
        </div>

        <!-- Footer -->
        <template #footer>
            <b-button variant="primary" :disabled="!canSave" @click="savePath">
                <i class="ti ti-device-floppy me-1"></i> 저장
            </b-button>
            <b-button variant="light" @click="closeModal">취소</b-button>
        </template>
    </b-modal>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import Simplebar from 'simplebar-vue'
import * as expertModules from '@/modules/expert'

// Props 정의
const props = defineProps({
    modelValue: {
        type: Boolean,
        default: false
    },
    empNo: {
        type: String,
        default: ''
    },
    initialTargetName: {
        type: String,
        default: ''
    }
})

// Emit 정의
const emit = defineEmits(['update:modelValue', 'save'])

const show = computed({
    get: () => props.modelValue,
    set: (value) => emit('update:modelValue', value)
})

const activeTab = ref(0)
const selectedWorkbook = ref(null) // 선택한 워크북 객체 (ID와 이름 포함)
const targetName = ref('')

// 워크북 목록 데이터
const workbookListData = ref([])
// 현재 활성화된 워크북 타입 ('P' 또는 'S')
const currentWorkbookType = ref(null)
// 로딩 상태
const isLoading = ref(false)

/* 1Depth 경로 목록 - API에서 가져온 데이터로 대체 */
const myWorkbookPaths = computed(() => {
    return workbookListData.value.filter((wb) => wb.targetWorkbookType === 'P')
})

const commonWorkbookPaths = computed(() => {
    return workbookListData.value.filter((wb) => wb.targetWorkbookType === 'S')
})

// 탭 변경 시 워크북 목록 조회
watch(activeTab, (newTab) => {
    const workbookType = newTab === 0 ? 'P' : 'S'
    prepareWorkbookList(workbookType)
})

// 모달이 열릴 때 '내 워크북' 목록 자동 조회
watch(
    () => props.modelValue,
    (newValue) => {
        if (newValue) {
            // 기본 탭 로드
            prepareWorkbookList('P')
            // 부모에서 전달된 기존 이름 프리셋
            targetName.value = props.initialTargetName || ''
        } else {
            // 닫힐 때 초기화
            targetName.value = ''
            selectedWorkbook.value = null
            activeTab.value = 0
        }
    }
)

/**
 * 워크북 목록 조회
 */
async function prepareWorkbookList(workbookType) {
    currentWorkbookType.value = workbookType

    const workbookParam = {
        targetWorkbookType: workbookType,
        regId: workbookType === 'P' ? props.empNo : null
    }

    isLoading.value = true

    try {
        const response = await expertModules.selectWorkbookList(workbookParam)
        const data = response
        workbookListData.value = data.workbookListData || []
        // 자동 선택(첫번째 경로) → 저장 버튼 즉시 활성화 유도
        if (!selectedWorkbook.value && workbookListData.value.length > 0) {
            selectedWorkbook.value = workbookListData.value[0]
        }
    } catch (error) {
        console.error('워크북 목록 조회 실패:', error)

        if (error.response && error.response.status === 401) {
            // 401 에러 처리
            console.error('인증 실패')
        }
    } finally {
        isLoading.value = false
    }
}

/* 저장 가능 여부 */
const canSave = computed(
    () =>
        selectedWorkbook.value &&
        targetName.value.trim() &&
        targetName.value.length <= 50
)

/* 저장 */
const savePath = () => {
    if (!selectedWorkbook.value) return

    // 부모 컴포넌트로 저장 데이터 전달
    emit('save', {
        workbookId: selectedWorkbook.value.targetWorkbookId,
        workbookName: selectedWorkbook.value.targetWorkbookName,
        targetName: targetName.value
    })

    show.value = false
}

/* 닫기 */
const closeModal = () => {
    show.value = false
    selectedWorkbook.value = null
    targetName.value = ''
    activeTab.value = 0
}
</script>
