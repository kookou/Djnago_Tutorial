<template>
    <!-- Expert Header -->
    <div class="expert-header">
        <!-- Title -->
        <div class="title-box flex-grow-1">
            <label>타겟팅명</label>
            <h3 class="mb-0 fw-bolder text-truncate">
                {{ displayTargetName }}
            </h3>
        </div>
        <!-- Button Group -->
        <div class="btn-box flex-shrink-0">
            <div class="hstack gap-2">
                <label for="targetLimitCount" class="form-label mb-0 text-muted"
                    >최대 조회건수 설정</label
                >
                <input
                    class="form-control text-end"
                    type="text"
                    inputmode="numeric"
                    :value="queryCount"
                    @input="onCountInput"
                    id="targetLimitCount"
                    maxlength="7"
                    style="width: 100px"
                />
                <span class="text-muted">건</span>
            </div>
            <div class="vr mx-2 my-1"></div>
            <b-Button variant="light" @click.native="requestPreviewData">
                <i class="ti ti-eye"></i>미리보기
            </b-Button>
            <b-button variant="light" @click.native="requestCampaignTarget">
                <i class="ti ti-user-plus"></i>캠페인 대상 생성
            </b-button>
            <b-button variant="light">
                <i class="ti ti-file-excel"></i>엑셀 데이터 생성
            </b-button>
            <b-button variant="light">
                <i class="ti ti-player-play"></i>시뮬레이션 수행
            </b-button>
            <div class="vr mx-2 my-1"></div>
            <b-button variant="primary" @click="requestSaveWorkbookPath">
                <i class="ti ti-device-floppy"></i>워크북 경로 저장
            </b-button>
        </div>
    </div>

    <!-- 워크북 경로 저장 모달 연결 -->
    <WorkbookPathSaveModal
        v-model="isSaveModalVisible"
        :empNo="empNo"
        :initial-target-name="displayTargetName"
        @save="handleWorkbookSave"
    />

    <!-- 경고 모달 -->
    <b-modal
        v-model="isValidationModalOpen"
        title="이건 경고요"
        hide-footer
        centered
        scrollable
        size="sm"
    >
        {{ inputMessage }}
    </b-modal>
</template>

<script setup>
import { ref, computed, nextTick, watch } from 'vue'
import { Modal } from 'ant-design-vue' // Alert 대체 20250930 by hj
import * as expertModules from '@/modules/expert'
import WorkbookPathSaveModal from '@/components/expert/WorkbookPathSaveModal.vue'
import { next } from '@/assets/scss/plugins/bootstrap/js/dist/dom/selector-engine'
//상단 모달 호출 START 20250930 by hj -->

const props = defineProps({
    queryData: {
        type: Object,
        default: () => ({
            targetId: '',
            targetAreaGroupId: '',
            reportCount: 0,
            targetReportList: [],
            targetConditionList: [],
            completeList: [],
            // 새로운 1차원 조건 배열(서버 포맷): conditionDepth/condition 포함
            selectTargetCondition: [],
            // 로드된 타겟팅명 (헤더 표시용)
            targetName: ''
        })
    },
    targetId: {
        type: String,
        default: ''
    }
})

// emit 정의
const emit = defineEmits(['save-target', 'request-data-trigger'])

const queryCount = ref('999,999')
const selectWorkbookId = ref('') // 워크북 모달에서 선택한 워크북 ID
const targetName = ref('') // 워크북 모달에서 입력한 타겟 작업명
const empNo = ref('TW0000000943') //TEST DATA loginEmpId -> api 내에서 가져오자.
const workType = ref('')

const editedConditionCount = ref(0) // 설정 완료 지점 미저장 조건 (jQuery: div[status="edit"])
const editConditionCount = ref(0) // Drag & Drop 지점 미저장 조건 (jQuery: div[id^="target_edit_"])
const targetLimitCount = ref('0')
const selectTargetId = ref(null) // 타겟 ID (null이면 INSERT, 값이 있으면 UPDATE)
const targetItemLimitCnt = ref(20) // 출력 조건 제한 건수

const targetingConditionAreaSave = ref(null)
const targetingReportAreaBody = ref(null)
const selectMetaFieldForSaveList = ref(null) // AJAX 응답 데이터
const requiredHTML = ref('')
const selectedRequiredOptions = ref([])

// 모달 표시 여부
const isSaveModalVisible = ref(false)

// 표시용 타이틀 우선순위: 입력값(사용자/모달) > 로드된 이름 > 기본 문구
const displayTargetName = computed(() => {
    const typed = (targetName.value || '').trim()
    const loaded = (
        (props.queryData && props.queryData.targetName) ||
        ''
    ).trim()
    return typed || loaded || '임시 타겟 작업명'
})

// props.targetId 변경 감지하여 selectTargetId 업데이트
watch(
    () => props.targetId,
    (newValue) => {
        selectTargetId.value = newValue
        // UPDATE 시에도 입력한 이름 유지 (로드된 이름은 별도 props.queryData.targetName)
        // 필요 시 여기서 targetName.value = props.queryData.targetName 로 동기화 가능
    }
)

// 로드된 타겟명이 도착하면 로컬 입력값을 비워 충돌 방지
watch(
    () => (props.queryData && props.queryData.targetName) || '',
    (newVal, oldVal) => {
        // 로드된 이름이 생겼고 사용자가 아직 아무 것도 입력하지 않은 경우만 프리셋
        if ((newVal || '').trim() && !(targetName.value || '').trim()) {
            // targetName.value = newVal // 자동 덮어쓰기 대신 유지 (표시 우선순위에서 loaded 활용)
        }
    }
)

const showAlert = (title, message) => {
    Modal.warning({
        title: title,
        content: message,
        okText: '확인',
        dangerouslyUseHTMLString: true // HTML 태그 허용
    })
}

function hideLoadingMask() {
    console.log('로딩 마스크 숨기기')
}

function fn_401Page() {
    console.log('401 페이지 이동 처리')
}

/**
 * 메타필드 필수항목 포함여부 체크
 */
async function checkSaveConditionRequired(itemArray, targetConditionItem) {
    // 조건 필드 ID 추출
    const conditionFieldArr = []

    ;(targetConditionItem || []).forEach((item) => {
        //이미 타겟 조건이라 아래 조건문은 필요 없을 듯.
        //if (item.className === 'tgtree-condition') {
        //const idParts = item.id.split('_')
        //const metaFieldId = idParts.length > 2 ? idParts[2] : null
        const metaFieldId = item.metaFieldId
        if (metaFieldId) {
            conditionFieldArr.push(metaFieldId)
        }
        //}
    })

    const metaFieldobj = {
        // itemArray에서 metaFieldId만 추출
        metaFieldIdArr: itemArray.map((obj) => obj.metaFieldId),
        conditionFieldArr: conditionFieldArr
    }

    let returnFlag = 'Y'
    requiredHTML.value = ''

    try {
        // showLoadingMask();

        const response = await expertModules.checkSaveConditionRequired(
            metaFieldobj
        )

        // 성공 처리
        const requiredList = response.requiredList || []

        // 3. 필수 항목 누락 여부 및 HTML 생성
        if (requiredList.length > 0) {
            returnFlag = 'N' // 필수 항목 누락 확인

            const tableList = new Set(
                requiredList.map((item) => item.metaTable)
            )
            let html = '<div class="text-start px-15 ms-4">'

            tableList.forEach((value) => {
                const tableName = value.split('/')[1]

                // 테이블 이름 (폴더 아이콘)
                html += `<span class="text-start fs-7"> 
                           <img src="../assets/plugins/custom/jstree/nodeicon/folder.png"> ${tableName}
                         </span>
                         <br>`

                // 해당 테이블의 필수 필드 목록
                requiredList
                    .filter((item) => item.metaTable === value)
                    .forEach((item) => {
                        html += `<span class="text-start fs-7 d-lg-inline-block w-lg-175px mb-1 text-truncate" title="${item.metaFieldName}">
                                 <img class="ms-8" src="../assets/plugins/custom/jstree/nodeicon/${item.metaIconType}.png">
                                 ${item.metaFieldName}
                             </span>
                             <br>`
                    })
                html += '<br>'
            })

            html += '</div>'
            requiredHTML.value = html // 반응형 변수에 HTML 저장
        }
    } catch (error) {
        // 에러 처리
        if (error.response && error.response.status === 401) {
            fn_401Page()
        } else {
            console.error('AJAX Error:', error)
        }
        // 에러가 발생해도 returnFlag는 기본값 'Y'를 유지하거나,
        // 필요에 따라 'E'(Error) 등으로 처리할 수 있습니다. 여기서는 'Y'를 유지합니다.
    } finally {
        // 로딩 마스크 숨기기
        hideLoadingMask()
    }

    return returnFlag
}

/**
 * TargetCondition & TargetItem 항목 메타정보 조회
 */
async function selectMetaFieldForSave() {
    // DOM 요소가 마운트되었는지 확인
    const targetConditionItems = props.queryData.completeList // 타겟팅 조건

    const targetItems = props.queryData.targetReportList // 타겟팅 출력 조건

    let targetItemArray = []

    // 타겟팅 조건 항목 처리
    targetConditionItems.forEach((item) => {
        //이미 타게팅 조건 데이터라 아래 조건은 필요 없을 것으로 보임
        //if (item.className === 'tgtree-condition') {
        //const idParts = item.id.split('_')
        //const metaFieldId = idParts.length > 2 ? idParts[2] : null
        const metaFieldId = item.metaFieldId
        if (metaFieldId) {
            targetItemArray.push({ metaFieldId: metaFieldId })
        }
        //}
    })

    // 타겟팅 출력 조건 항목 처리
    targetItems.forEach((item) => {
        //const idParts = item.id.split('_')
        //const metaFieldId = idParts.length > 3 ? idParts[3] : null
        const metaFieldId = item.metaFieldId
        if (metaFieldId) {
            targetItemArray.push({ metaFieldId: metaFieldId })
        }
    })

    // 메타필드 필수항목 포함여부 체크
    let returnFlag = 'Y'
    if (
        checkSaveConditionRequired(targetItemArray, targetConditionItems) ===
        'N'
    ) {
        returnFlag = 'N'
        return returnFlag
    }

    try {
        //showLoadingMask() // 필요하다면 로딩 마스크 표시

        const response = await expertModules.selectMetaFieldForSave(
            targetItemArray
        )

        selectMetaFieldForSaveList.value = response.selectMetaFieldForSaveList
    } catch (error) {
        if (error.response && error.response.status === 401) {
            fn_401Page()
        } else {
            console.error('AJAX Error:', error)
        }
    } finally {
        hideLoadingMask()
    }

    return returnFlag
}

// 저장 요청 - 부모 컴포넌트로 데이터 전달
const saveTarget = (targetConditionData) => {
    const workbookId = selectWorkbookId.value.trim()

    const tName = targetName.value.trim()
    //const areaGroupId = selectTargetAreaGroupIdForSave.value.trim()
    const areaGroupId = props.queryData.targetAreaGroupId ?? ''
    const areaId = props.queryData.targetAreaId

    // 유효성 검사
    if (workbookId === '') {
        showAlert('', '저장할 워크북을 선택하세요.', 'warning')
        return
    }

    if (tName === '') {
        showAlert('', '타겟팅명을 입력하세요.', 'warning')
        return
    }

    if (tName.length > 50) {
        showAlert('', '타겟팅명의 길이는 50자 이하입니다.', 'warning')
        return
    }

    if (areaGroupId.length !== 12) {
        showAlert(
            '',
            '타겟팅 목적이 선택되지 않았습니다. 관리자에게 문의하세요.',
            'warning'
        )
        return
    }

    // 부모 컴포넌트로 저장 데이터 전달
    emit('save-target', {
        workbookId,
        targetName: tName,
        areaGroupId,
        areaId,
        targetConditionData,
        empNo: empNo.value,
        workType: workType.value,
        targetLimitCount: targetLimitCount.value,
        selectTargetId: selectTargetId.value,
        selectedRequiredOptions: selectedRequiredOptions.value,
        targetItemLimitCnt: targetItemLimitCnt.value,
        selectTargetCondition: props.queryData.selectTargetCondition
    })
}

const showModalSaveWorkbook = async () => {
    const edited = editedConditionCount.value
    const edit = props.queryData.targetConditionList.length
    //const limitCount = targetLimitCount.value;
    const limitCount = queryCount.value
    const targetId = selectTargetId.value

    // 설정완료 > 수정 중 항목
    if (edited > 0) {
        showAlert(
            '타겟팅 조건을 수정하세요.',
            '수정중인 타겟팅 조건이 있습니다.<br>조건 설정 후 저장하시기 바랍니다.',
            'warning'
        )
        return
    }

    // 조건추가 > 설정 중 항목
    if (edit > 0) {
        showAlert(
            '타겟팅 조건을 설정하세요.',
            '타겟팅 조건이 설정되어 있지 않습니다.<br>조건 설정 후 저장하시기 바랍니다.',
            'warning'
        )
        return
    }

    // 최대 조회 건수 검사
    if (limitCount < 1) {
        showAlert(
            '최대 조회건수를 입력하세요.',
            '최대 조회건수가 0으로 설정되었습니다. 값을 입력 후 저장하시기 바랍니다.',
            'warning'
        )
        return
    }

    // 메타필드 필수항목 포함여부 체크
    const requiredCheckResult = await selectMetaFieldForSave()
    if (requiredCheckResult === 'N') {
        // checkSaveConditionRequired 함수로 requiredHTML 가져와야 함.
        showAlert('필수 포함 조건을 추가하세요.', requiredHTML, 'warning')
        return
    }

    // targetId가 없거나 빈 경우: Insert 로직 (새 워크북 저장)
    if (targetId == null || targetId.length < 1) {
        // 입력값 초기화 제거: 저장/모달 입력으로 헤더 타이틀 즉시 반영되도록 함
        // targetName.value = ''

        //saveTarget() // TEST 호출

        //prepareWorkbookList //모달에서 자동으로 조회
        isSaveModalVisible.value = true
    }
    // targetId가 있는 경우: Update 로정
    else {
        saveTarget() // 저장 함수 호출 (Update)
    }
}

const checkSaveCondition = () => {
    const currentWorkingType = workType.value
    const saveReport = props.queryData.targetReportList.length ?? 0

    // --- 1. 미리보기 조건 ('1') ---
    if (currentWorkingType === '1') {
        if (saveReport < 1) {
            validationModalOpen(
                '',
                '1개 이상의 출력조건을 설정하셔야 미리보기가 가능합니다.',
                'warning'
            )
            return
        }
    }

    // --- 2. 엑셀 생성 조건 ('4') ---
    if (currentWorkingType === '4') {
        if (saveReport < 1) {
            validationModalOpen(
                '',
                '1개 이상의 출력조건을 설정하셔야 엑셀 데이터 생성이 가능합니다.',
                'warning'
            )
            return
        }
    }

    // --- 3. 시뮬레이션 조건 ('S') ---
    if (currentWorkingType === 'S') {
        if (saveReport < 1) {
            validationModalOpen(
                '',
                '1개 이상의 출력조건을 설정하셔야 시뮬레이션이 가능합니다.',
                'warning'
            )
            return
        }

        // selectResultSimulationTargetAreaId.value = '';
        // selectResultSimulationTargetId.value = '';
    }

    showModalSaveWorkbook()
}

//미리보기 모달 요청
const requestPreviewData = () => {
    workType.value = '1'
    // completeList emit 요청
    emit('request-data-trigger')

    // emit 완료 후 실행
    nextTick(() => {
        checkSaveCondition()
    })
}

//캠페인 대상 생성
const requestCampaignTarget = () => {
    workType.value = '2'

    emit('request-data-trigger')

    nextTick(() => {
        checkSaveCondition()
    })
}

//워크북 경로 저장
const requestSaveWorkbookPath = () => {
    //workType.value = ''

    //데이터 전송이 필요함
    emit('request-data-trigger')

    nextTick(() => {
        showModalSaveWorkbook()
    })
}
// <-- 상단 모달 호출 END 20250930 by hj

const isValidationModalOpen = ref(false)
const inputMessage = ref('')

// ====== 경고 모달 ======
function validationModalOpen(message) {
    isValidationModalOpen.value = true
    inputMessage.value = message
}

// 워크북 저장 모달에서 저장 버튼 클릭 시 호출
const handleWorkbookSave = (data) => {
    // 모달에서 전달받은 데이터 설정
    selectWorkbookId.value = data.workbookId
    targetName.value = data.targetName

    console.log('워크북 ID:', data.workbookId)
    console.log('타겟 작업명:', data.targetName)

    // saveTarget 함수 호출
    saveTarget()
}
</script>
