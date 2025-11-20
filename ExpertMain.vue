<template>
    <div class="expert-wrapper">
        <ExpertHeader
            @save-target="handleSaveTarget"
            @update-workbook-list="handleUpdateWorkbookList"
            @request-data-trigger="increaseEmitTrigger"
            :query-data="queryData"
            :target-id="currentTargetId"
        ></ExpertHeader>
        <div class="expert-content-wrap">
            <ExpertQueryMain
                v-model:data="queryData"
                :emit-trigger="emitTrigger"
            ></ExpertQueryMain>
            <ExpertSide
                :result="saveResult"
                :workbook-list="workbookListData"
                :execution-list="targetExecutionList"
                :current-target-id="currentTargetId"
                @refresh-execution="refreshTargetExecution"
            ></ExpertSide>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import ExpertHeader from './ExpertHeader.vue'
import ExpertQueryMain from './ExpertQueryMain.vue'
import ExpertSide from './ExpertSide.vue'
import * as expertModules from '@/modules/expert'
import { showAlert } from '@/utils/common'
import { useExpertStore } from '@/store/expert'

const store = useExpertStore()

onMounted(async () => {
    // 홈에서 저장한 선택 값 (pinia: selectedTargetGroupId) → queryData에 반영
    const persistedGroupId = store.selectedTargetGroupId
    if (persistedGroupId) {
        queryData.value.targetAreaGroupId = persistedGroupId
    }
})

const queryData = ref({
    targetAreaGroupId: '',
    targetAreaId: '',
    targetName: '', // 불러오기 시 헤더 표시용 타겟명
    reportCount: 0, // 출력 항목 갯수
    targetReportList: [], // 출력 조건 리스트
    targetConditionList: [], // 타겟팅 조건 리스트
    completeList: [], // 완료된 조건 리스트
    targetingConditionCheckeds: [], // 필수 조건 체크 리스트
    selectTargetCondition: [], // ExpertQueryMain에서 내보낸 1차원 조건 리스트(conditionDepth/condition 포함)
    outputFunctionSaveData: {} // 출력함수/인수 저장 맵(chip.key 기반)
}) // 쿼리 데이터 통합 객체
const saveResult = ref(null) // 저장 결과
const workbookListData = ref([]) // 워크북 목록 데이터
const emitTrigger = ref(0) // completeList emit 트리거 (Props 방식으로 변경)
const targetExecutionList = ref([]) // 작업 내역 목록
const currentTargetId = ref('') // 현재 타겟 ID

//
// 2️⃣ UI 동작 메서드
//

// Props 트리거 : 상단 모달 열 때, 타게팅 조건 List emit
function increaseEmitTrigger() {
    emitTrigger.value++
}

// 저장 핸들러 - ExpertHeader에서 받은 데이터로 저장 처리
async function handleSaveTarget(data) {
    console.log('저장 요청 데이터:', data)

    try {
        // Insert/Update 플래그 결정
        const workingFlag =
            data.selectTargetId == null || data.selectTargetId.length < 1
                ? 'I'
                : 'U'

        // ====================================================================================================================
        // [ insert ] 1. bi_target 구성 ====================================================================================
        // ====================================================================================================================
        // 요청 데이터 구성
        const requestObj = {
            targetModel: [
                {
                    targetId: data.selectTargetId,
                    targetName: data.targetName,
                    targetPathId: '',
                    targetWorkbookId: data.workbookId,
                    targetAreaGroupId: data.areaGroupId,
                    targetAreaId: data.areaId, // TODO: ExpertQueryMain에서 선택한 주제영역 ID 전달 필요
                    targetCnt: String(data.targetLimitCount).replace(/,/gi, ''),
                    targetType: 'user',
                    regId: data.empNo,
                    changId: data.empNo,
                    workingFlag: workingFlag
                }
            ],
            // ====================================================================================================================
            // [ insert ] 2. bi_target_condition : 타겟팅 조건 ===================================================================
            // ====================================================================================================================
            targetConditionModel: buildTargetConditionModel(
                // 우선순위: ExpertQueryMain이 내보낸 1차원 조건 배열 사용
                Array.isArray(queryData.value.selectTargetCondition) &&
                    queryData.value.selectTargetCondition.length > 0
                    ? queryData.value.selectTargetCondition
                    : queryData.value.completeList,
                data.empNo
            ),
            // ====================================================================================================================
            // [ insert ] 3. bi_target_option : 타겟팅 필수 조건 =================================================================
            // ====================================================================================================================
            targetOptionModel: buildTargetOptionModel(
                queryData.value.targetingConditionCheckeds,
                data.empNo
            ),
            // ====================================================================================================================
            // [ insert ] 4. bi_target_item : 타겟팅 출력 조건 ===================================================================
            // ====================================================================================================================
            targetItemModel: buildTargetItemModel(
                queryData.value.targetReportList,
                queryData.value.outputFunctionSaveData,
                data.empNo
            )
        }

        // 저장 API 호출
        const response = await expertModules.saveTarget(requestObj)

        // 성공 처리
        if (response.result === 'N000') {
            saveResult.value = {
                success: true,
                message: '타겟 작업이 저장되었습니다.',
                data: response
            }
            console.log('저장 성공:', response)

            // 생성된 Target Id 지정
            const savedTargetId = response.targetId
            currentTargetId.value = savedTargetId

            // workType에 따른 후속 처리
            const workType = data.workType || ''

            if (workType === '') {
                // 타겟팅 저장만 수행
                showAlert('', '타겟 작업이 저장되었습니다.', 'success')
            } else if (workType === 'S') {
                // 시뮬레이션
                // TODO: showModalSimulation() 구현 필요
                console.log('시뮬레이션 모달 표시 필요')
            } else {
                // 1: 미리보기, 2: 캠페인 대상 생성, 4: 엑셀 데이터 생성
                await requestTargetExecution(
                    workType,
                    savedTargetId,
                    data.empNo
                )
            }

            //워크 타입 초기화
            data.workType = ''
            console.log('workType : ' + data.workType)
        } else {
            saveResult.value = {
                success: false,
                message: '타겟 작업 저장이 실패하였습니다.',
                data: response
            }
            showAlert('', '타겟 작업 저장이 실패하였습니다.', 'error')
        }
    } catch (error) {
        console.error('저장 실패:', error)

        // TODO: 401 에러 처리 (fn_401Page)
        if (error.response && error.response.status === 401) {
            console.error('인증 오류 발생')
        }

        saveResult.value = {
            success: false,
            message: '저장 중 오류가 발생했습니다.',
            error: error
        }

        showAlert('', '타겟 작업 저장이 실패하였습니다.', 'error')
    }
}

function isCustomDropdown() {
    const searchOptions = document.getElementById('search-close-options')
    const dropdown = document.getElementById('search-dropdown')
    const searchInput = document.getElementById('search-options')

    if (!searchInput) return

    const toggleDropdown = () => {
        if (searchInput.value.length > 0) {
            dropdown?.classList.add('show')
            searchOptions?.classList.remove('d-none')
        } else {
            dropdown?.classList.remove('show')
            searchOptions?.classList.add('d-none')
        }
    }

    searchInput.addEventListener('focus', toggleDropdown)
    searchInput.addEventListener('keyup', toggleDropdown)

    searchOptions?.addEventListener('click', () => {
        searchInput.value = ''
        dropdown?.classList.remove('show')
        searchOptions?.classList.add('d-none')
    })

    document.body.addEventListener('click', (e) => {
        if (e.target.getAttribute('id') !== 'search-options') {
            dropdown?.classList.remove('show')
            searchOptions?.classList.add('d-none')
        }
    })
}

function onCountInput(e) {
    let digits = e.target.value.replace(/\D/g, '')
    if (digits) digits = String(Math.min(Number(digits), 999999))
    queryCount.value = digits.replace(/\B(?=(\d{3})+(?!\d))/g, ',')
}

function getQueryCountValue() {
    return queryCount.value.replace(/,/g, '') || null
}

function removeRow(index) {
    rows.value.splice(index, 1)
}

/**
 * 타겟팅 작업 요청
 * @param {string} requestType - 요청 타입 (1: 미리보기, 2: 캠페인 대상 생성, 4: 엑셀 데이터 생성, S: 시뮬레이션)
 * @param {string} targetId - 타겟 ID
 * @param {string} empNo - 사원번호
 */
async function requestTargetExecution(requestType, targetId, empNo) {
    try {
        const targetExecutionModel = {
            targetId: targetId,
            executionType: requestType,
            executionTypeNum: requestType,
            simulationCalcMonth: requestType === 'S' ? '1' : '0', // 시뮬레이션(S) 요청인 경우 1 그 외 0
            regId: empNo
        }

        // 시뮬레이션인 경우 추가 파라미터
        if (requestType === 'S') {
            // TODO: 시뮬레이션 관련 추가 데이터 필요
            // targetExecutionModel.oriTargetId = ...
            // targetExecutionModel.resultTargetId = ...
            // targetExecutionModel.resultTargetName = ...
            // targetExecutionModel.resultTargetCnt = ...
        }

        console.log('# targetExecutionModel', targetExecutionModel)

        // API 호출
        const response = await expertModules.requestExecution(
            targetExecutionModel
        )

        const result = response.result

        // 성공 처리
        if (result.return_code === 'N000') {
            let alertTitle = ''
            let alertMessage = ''

            switch (requestType) {
                case '1': // 미리보기
                    alertTitle = '[ 미리보기 ]'
                    alertMessage =
                        '미리보기 작업을 요청하였습니다. PUSH 알림을 받으시면 처리내역을 확인 하시기 바랍니다.'
                    break
                case '2': // 캠페인 대상 생성
                    alertTitle = '[ 캠페인 대상 생성 ]'
                    alertMessage =
                        '캠페인 대상 생성작업을 요청하였습니다. PUSH 알림을 받으시면 처리내역을 확인 하시기 바랍니다.'
                    break
                case '4': // 엑셀 데이터 생성
                    alertTitle = '[ 엑셀 데이터 생성 ]'
                    alertMessage =
                        '엑셀 데이터 생성작업을 요청하였습니다. PUSH 알림을 받으시면 처리내역을 확인 하시기 바랍니다.'
                    break
                case 'S': // 시뮬레이션
                    alertTitle = '[ 시뮬레이션 ]'
                    alertMessage =
                        "결과 시뮬레이션 작업을 요청하였습니다.<br>처리내역은 '워크리스트 > 내 워크북 > 시뮬레이션'<br>경로에서 확인 가능합니다."
                    break
                case '7': // 채널 시뮬레이션
                    alertTitle = '[ 시뮬레이션 ]'
                    alertMessage =
                        "채널 시뮬레이션 작업을 요청하였습니다.<br>처리내역은 '워크리스트 > 내 워크북 > 시뮬레이션'<br>경로에서 확인 가능합니다."
                    break
            }

            // TODO: saAlert 또는 알림 UI 컴포넌트로 대체 필요
            console.log(alertTitle, alertMessage)
            //alert(`${alertTitle}\n${alertMessage.replace(/<br>/g, '\n')}`)
            showAlert(alertTitle, alertMessage, 'success')
        } else if (result.return_code === 'E001') {
            alert(
                '해당 작업이 진행중에 있습니다.\n진행 내역은 [작업내역] 에서 확인 가능합니다.'
            )
        } else if (result.return_code === 'E002') {
            alert(
                '요청건이 많아 추가 작업을 진행할 수 없습니다.\n잠시 후 다시 시도 하시기 바랍니다.'
            )
        } else if (result.return_code === 'E003') {
            alert(
                '할당된 모든 프로세스가 사용중에 있습니다.\n잠시 후 다시 시도 하시기 바랍니다.'
            )
        } else {
            // 실패 처리
            let errorTitle = ''
            switch (requestType) {
                case '1':
                    errorTitle = '미리보기 작업 요청에 실패하였습니다.'
                    break
                case '2':
                    errorTitle = '캠페인 대상 생성작업 요청에 실패하였습니다.'
                    break
                case '4':
                    errorTitle = '엑셀 데이터 생성작업 요청에 실패하였습니다.'
                    break
                case 'S':
                    errorTitle = '결과 시뮬레이션 작업 요청에 실패하였습니다.'
                    break
                case '7':
                    errorTitle = '채널 시뮬레이션 작업 요청에 실패하였습니다.'
                    break
            }
            alert(errorTitle)
        }

        // 시뮬레이션이 아닌 경우 작업내역 조회
        if (requestType !== 'S' && requestType !== '7') {
            await loadTargetExecution(targetId)
        }
    } catch (error) {
        console.error('타겟팅 작업 요청 실패:', error)

        if (error.response && error.response.status === 401) {
            console.error('인증 오류 발생')
            // TODO: fn_401Page 구현 필요
        }

        alert('타겟팅 작업 요청 중 오류가 발생했습니다.')
    }
}

/**
 * 타겟팅 작업 내역 조회
 * @param {string} targetId - 타겟 ID
 */
async function loadTargetExecution(targetId) {
    try {
        // 현재 타겟 ID 저장
        currentTargetId.value = targetId

        const requestData = {
            targetId: targetId
        }

        // API 호출
        const response = await expertModules.selectTargetExecution(requestData)

        if (response && response.selectTargetExecution) {
            const executionList = response.selectTargetExecution

            // 작업 내역 데이터 가공
            targetExecutionList.value = executionList.map((item) => ({
                targetId: item.targetId,
                executionId: item.executionId,
                executionType: item.executionType,
                executionStatus: item.executionStatus,
                executionCnt: item.executionCnt,
                changDate: item.changDate,
                // 아이콘 선택
                icon: getExecutionTypeIcon(item.executionType),
                // 완료 여부
                isCompleted: item.executionStatus === '편성완료'
            }))

            console.log('작업 내역 조회 성공:', targetExecutionList.value)
        }
    } catch (error) {
        console.error('작업 내역 조회 실패:', error)

        if (error.response && error.response.status === 401) {
            console.error('인증 오류 발생')
            // TODO: fn_401Page 구현 필요
        }
    }
}

/**
 * 실행 타입별 아이콘 반환
 * @param {string} executionType - 실행 타입
 * @returns {string} 아이콘 클래스명
 */
function getExecutionTypeIcon(executionType) {
    const iconMap = {
        미리보기: 'ti ti-eye',
        '캠페인 대상 생성': 'ti ti-user-plus',
        '엑셀 데이터 생성': 'ti ti-file-excel',
        시뮬레이션: 'ti ti-chart-line',
        '채널 시뮬레이션': 'ti ti-chart-dots'
    }
    return iconMap[executionType] || 'ti ti-file'
}

/**
 * 작업 내역 새로고침
 */
function refreshTargetExecution() {
    if (currentTargetId.value) {
        loadTargetExecution(currentTargetId.value)
    }
}

/**
 * 타겟팅 조건 모델 빌드
 * @param {Array} completeList - 완료된 조건 리스트 (queryData.completeList)
 * @param {string} empNo - 사원번호
 * @returns {Array} targetConditionModel
 *
 * @note PostgreSQL 호환 버전
 * - 날짜 함수는 PostgreSQL 문법 사용 (CURRENT_DATE + INTERVAL '...')
 * - Hadoop/Hive의 DATE_ADD 대신 PostgreSQL 표준 날짜 연산 사용
 */
function buildTargetConditionModel(listOrFlat, empNo) {
    if (!listOrFlat || listOrFlat.length === 0) {
        return []
    }

    // 입력 데이터가 1차원(flat)인지 판별: condition/conditionDepth가 존재하면 flat로 간주
    const isFlat = listOrFlat.some(
        (it) =>
            it &&
            (it.condition !== undefined || it.conditionDepth !== undefined)
    )

    const rows = []

    if (isFlat) {
        // ExpertQueryMain이 내보낸 1차원 조건 배열 기반 매핑
        const arr = [...listOrFlat]
        // conditionOrder가 있으면 그 순서로 정렬(안전)
        arr.sort((a, b) => (a.conditionOrder ?? 0) - (b.conditionOrder ?? 0))

        arr.forEach((item, idx) => {
            const inputType =
                item.inputType ?? item.extraValues?.inputType ?? '1'
            let rawValue = item.value ?? item.extraValues?.inputValue ?? ''

            if (inputType === '2') {
                // 날짜함수: PostgreSQL 형식으로 변환 (interval 문자열을 그대로 사용)
                const intervalValue = rawValue || '0'
                rawValue = `CURRENT_DATE + INTERVAL '${intervalValue}'`
            }

            const opCode = item.operator ?? item.extraValues?.operator ?? 'A1'

            const row = {
                metaFieldId: item.metaFieldId ?? item.id,
                virtualMetaFieldId: item.virtualMetaFieldId ?? null,
                operator: changeOperationForSql(opCode),
                value: rawValue ?? '',
                condition: item.condition ?? null,
                conditionDepth: Number(item.conditionDepth ?? item.depth ?? 1),
                conditionOrder: item.conditionOrder ?? idx + 1,
                inputType: inputType,
                regId: empNo,
                changId: empNo
            }
            rows.push(row)
        })
    } else {
        // 구형 경로(completeList 기반): 정보 부족으로 안전한 최소 매핑
        // - logicalOperator, depth 부재 가능 → 기본값으로 세팅
        for (let i = 0; i < listOrFlat.length; i++) {
            const item = listOrFlat[i]
            const nextItem = listOrFlat[i + 1]

            const inputType = item.extraValues?.inputType || '1'
            let processedValue = item.extraValues?.inputValue || ''
            if (inputType === '2') {
                const intervalValue = processedValue || '0'
                processedValue = `CURRENT_DATE + INTERVAL '${intervalValue}'`
            }

            const row = {
                metaFieldId: item.metaFieldId || item.id,
                virtualMetaFieldId: item.virtualMetaFieldId || null,
                operator: changeOperationForSql(
                    item.extraValues?.operator || 'A1'
                ),
                value: processedValue ?? '',
                condition: nextItem?.logicalOperator || null,
                conditionDepth: nextItem?.depth || item.depth || 1,
                conditionOrder: i + 1,
                inputType: inputType,
                regId: empNo,
                changId: empNo
            }
            rows.push(row)
        }
    }

    console.log('# 타겟팅 조건 (buildTargetConditionModel):', rows)
    return rows
}

/**
 * SQL 연산자 변환 함수
 * @param {string} operator - UI 연산자 코드 (A1, A2, B1, etc.)
 * @returns {string} SQL 연산자
 */
function changeOperationForSql(operator) {
    const operatorMap = {
        A1: '=', // 같음
        A2: '!=', // 같지 않음
        A3: '>', // 큼
        A4: '>=', // 크거나 같음
        A5: '<', // 작음
        A6: '<=', // 작거나 같음
        B1: 'IN', // 포함
        B2: 'NOT IN', // 불포함
        B3: 'LIKE', // 유사
        B4: 'NOT LIKE', // 유사하지 않음
        B5: 'BETWEEN', // 사이
        B6: 'NOT BETWEEN', // 사이가 아님
        B7: 'IS NULL', // NULL
        B8: 'IS NOT NULL' // NOT NULL
    }

    return operatorMap[operator] || operator
}

/**
 * 타겟팅 필수 조건 모델 빌드
 * @param {Array} targetingConditionCheckeds - 필수 조건 체크 리스트 (queryData.targetingConditionCheckeds)
 * @param {string} empNo - 사원번호
 * @returns {Array} targetOptionModel
 */
function buildTargetOptionModel(targetingConditionCheckeds, empNo) {
    if (
        !targetingConditionCheckeds ||
        targetingConditionCheckeds.length === 0
    ) {
        return []
    }

    const targetOptionArr = []

    // 체크된 필수 조건 ID를 순회하면서 객체 생성
    for (let i = 0; i < targetingConditionCheckeds.length; i++) {
        const optionId = targetingConditionCheckeds[i]

        const targetOptionObj = {
            optionTargetId: optionId,
            regId: empNo,
            changId: empNo
        }

        targetOptionArr.push(targetOptionObj)
    }

    console.log('# 타겟팅 필수 조건 (buildTargetOptionModel):', targetOptionArr)
    return targetOptionArr
}

/**
 * 타겟팅 출력 조건 모델 빌드
 * @param {Array} targetReportList - 출력 조건 리스트 (queryData.targetReportList)
 * @param {string} empNo - 사원번호
 * @returns {Array} targetItemModel
 */
function buildTargetItemModel(targetReportList, saveMap, empNo) {
    if (!targetReportList || targetReportList.length === 0) {
        return []
    }

    const targetItemArr = []

    // targetReportList를 순회하면서 출력 조건 객체 생성
    for (let i = 0; i < targetReportList.length; i++) {
        const item = targetReportList[i]
        const key = item.key || `${item.metaFieldId || 'MF'}_${i}`

        // 함수/인수 저장 맵에서 해당 칩의 저장값 조회
        const saved = saveMap && saveMap[key] ? saveMap[key] : null
        const fn = saved && saved.function ? saved.function : null
        const params = Array.isArray(saved?.params) ? saved.params : []

        let targetParameter01 = null
        let targetParameter02 = null
        let targetParameter03 = null

        // 특수 함수(TF0000000020): condition/result를 각각 콤마로 합쳐 param02/03에 저장
        if (
            String(fn?.targetFunctionId || item.targetFunctionId || '') ===
            'TF0000000020'
        ) {
            const conditions = params
                .map((p) => String(p?.condition ?? ''))
                .join(',')
            const results = params.map((p) => String(p?.result ?? '')).join(',')
            targetParameter01 =
                item.metaFieldName || item.name || item.title || null
            targetParameter02 = conditions
            targetParameter03 = results
        } else {
            // 일반 함수: 기존 규칙(첫 3개 result를 param01..03으로)
            const p1 = params[0]?.result ?? null
            const p2 = params[1]?.result ?? null
            const p3 = params[2]?.result ?? null
            targetParameter01 = p1 ?? item.targetParameter01 ?? null
            targetParameter02 = p2 ?? item.targetParameter02 ?? null
            targetParameter03 = p3 ?? item.targetParameter03 ?? null
        }

        const targetItemObj = {
            metaTableId: item.metaTableId || '',
            metaTableName: item.metaTableName || '',
            metaFieldId: item.metaFieldId || item.id,
            metaFieldName: item.metaFieldName || item.name || item.title,
            targetFunctionId:
                fn?.targetFunctionId || item.targetFunctionId || null,
            targetParameter01,
            targetParameter02,
            targetParameter03,
            itemOrder: i + 1,
            regId: empNo,
            changId: empNo
        }

        targetItemArr.push(targetItemObj)
    }

    console.log('# 타겟팅 출력 조건 (buildTargetItemModel):', targetItemArr)
    return targetItemArr
}
</script>
