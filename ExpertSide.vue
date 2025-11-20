<template>
    <!-- Aside Right -->
    <aside class="expert-aside">
        <!-- Aside Right Header -->
        <div class="expert-aside-header">
            <h4 class="mb-0" id="expert_execution_total">
                작업 내역 <span>({{ executionList.length }})</span>
            </h4>
            <b-button variant="link" @click="showResultModal = true">
                결과보기 Modal
            </b-button>
            <b-button
                variant="link"
                class="btn-icon rounded-circle"
                title="새로고침"
                id="expert_excution_refresh"
                @click="handleRefreshExecution"
            >
                <i class="ti ti-refresh"></i>
            </b-button>
        </div>

        <!-- Aside Right Body -->
        <Simplebar class="expert-aside-body">
            <EmptyMessage v-if="executionList.length === 0"
                >작업 내역이 없습니다.</EmptyMessage
            >

            <!-- 작업 내역 목록 표시 -->
            <b-row class="g-2 row-cols-sm-2 row-cols-lg-1">
                <b-col v-for="(execution, index) in executionList" :key="index">
                    <b-card
                        body-class="d-flex flex-wrap align-items-center gap-2 px-3"
                    >
                        <div class="avatar-sm flex-shrink-0">
                            <span class="avatar-title rounded-circle">
                                <!-- <i class="ti ti-user-plus"></i> -->
                                <i :class="execution.icon"></i>
                            </span>
                        </div>
                        <div class="flex-grow-1">
                            <h5 class="mb-0">
                                {{ execution.executionType }}
                            </h5>
                            <p class="mb-0 text-muted">
                                {{ execution.changDate || '-' }}
                            </p>
                            <p
                                v-if="execution.isCompleted"
                                class="mb-0 text-muted"
                            >
                                모수
                                <strong class="text-primary">{{
                                    formatNumber(execution.executionCnt)
                                }}</strong
                                >건
                            </p>
                        </div>
                        <div
                            class="d-grid gap-1 align-content-between h-100 text-end"
                        >
                            <p
                                class="mb-0 fs-12"
                                :class="
                                    execution.isCompleted
                                        ? 'text-primary'
                                        : 'text-muted'
                                "
                            >
                                {{ execution.executionStatus }}
                            </p>
                            <b-button
                                v-if="execution.isCompleted"
                                variant="light-2"
                                size="sm"
                                @click="handleViewResult(execution)"
                            >
                                결과보기
                            </b-button>
                        </div>
                    </b-card>
                </b-col>
                <!-- <b-col>
                    <b-card
                        body-class="d-flex flex-wrap align-items-center gap-2 px-3"
                    >
                        <div class="avatar-sm flex-shrink-0">
                            <span class="avatar-title rounded-circle">
                                <i class="ti ti-eye"></i>
                            </span>
                        </div>
                        <div class="flex-grow-1">
                            <h5 class="mb-0">미리보기</h5>
                            <p class="mb-0 text-muted">2022-02-02 12:12:12</p>
                            <p class="mb-0 text-muted">
                                모수
                                <strong class="text-primary">12,123</strong>건
                            </p>
                        </div>
                        <div
                            class="d-grid gap-1 align-content-between h-100 text-end"
                        >
                            <p class="mb-0 text-primary fs-12">작업중</p>
                        </div>
                    </b-card>
                </b-col>
                <b-col>
                    <b-card
                        body-class="d-flex flex-wrap align-items-center gap-2 px-3"
                    >
                        <div class="avatar-sm flex-shrink-0">
                            <span class="avatar-title rounded-circle">
                                <i class="ti ti-file-excel"></i>
                            </span>
                        </div>
                        <div class="flex-grow-1">
                            <h5 class="mb-0">액셀 데이터 생성</h5>
                            <p class="mb-0 text-muted">2022-02-02 12:12:12</p>
                            <p class="mb-0 text-muted">
                                모수
                                <strong class="text-primary">12,123</strong>건
                            </p>
                        </div>
                        <div
                            class="d-grid gap-1 align-content-between h-100 text-end"
                        >
                            <p class="mb-0 text-muted fs-12">작업완료</p>
                            <b-button variant="light-2" size="sm">
                                결과보기
                            </b-button>
                        </div>
                    </b-card>
                </b-col> -->
            </b-row>
        </Simplebar>
    </aside>
    <ExecutionResultModal
        v-model="showResultModal"
        :title="modalData.title"
        :completion-date="modalData.completionDate"
        :execution-result="modalData.executionResult"
        :targeting-condition="modalData.targetingCondition"
        :targeting-auto-condition="modalData.targetingAutoCondition"
        :targeting-report="modalData.targetingReport"
        :execution-query="modalData.executionQuery"
    />
</template>
<script setup>
import { ref, reactive } from 'vue'
import Simplebar from 'simplebar-vue'
import EmptyMessage from '@/components/EmptyMessage.vue'
import { formatNumber } from '@/utils/common'
import ExecutionResultModal from '@/components/worklist/ExecutionResultModal.vue'
import * as worklistModules from '@/modules/worklist'

const showResultModal = ref(false)

// 결과 데이터 상태
const modalData = reactive({
    title: '',
    completionDate: '',
    executionResult: {
        maxCount: 0,
        fixCount: 0,
        preCount: 0,
        preView: ''
    },
    targetingCondition: '',
    targetingAutoCondition: '',
    targetingReport: '',
    executionQuery: ''
})

// Props 정의
const props = defineProps({
    result: {
        type: Object,
        default: null
    },
    workbookList: {
        type: Array,
        default: () => []
    },
    executionList: {
        type: Array,
        default: () => []
    },
    currentTargetId: {
        type: String,
        default: ''
    }
})

// Emit 정의
const emit = defineEmits(['refresh-execution'])

/**
 * 새로고침 버튼 클릭 핸들러
 */
function handleRefreshExecution() {
    emit('refresh-execution')
}

/**
 * 결과보기 버튼 클릭 핸들러
 * @param {Object} execution - 실행 정보
 */
async function handleViewResult(execution) {
    try {
        // API 호출
        const response = await worklistModules.selectExecutionResult({
            targetId: execution.targetId,
            executionId: execution.executionId,
            executionType: execution.executionType
        })

        if (!response) {
            alert('작업정보를 불러올 수 없습니다.')
            return
        }

        const {
            selectTarget,
            selectTargetCondition,
            selectTargetOption,
            selectTargetItem,
            selectExecutionResult: executionData
        } = response

        // 실행 결과 데이터가 없는 경우
        if (!executionData || !executionData.executionId) {
            alert('작업정보를 불러올 수 없습니다.')
            return
        }

        // 모달 데이터 설정
        modalData.title = `${executionData.targetName} (${executionData.executionId})`
        modalData.completionDate = executionData.changDate || '-'

        // 실행 결과에 따른 데이터 설정
        const innerMaxCount = executionData.executionLimitCnt || 0
        const innerFixCount = executionData.executionCnt || 0
        let innerPreCount = 20
        let innerPreView = ''

        if (innerFixCount < 20) {
            innerPreCount = innerFixCount
        }

        // 실행 타입에 따른 처리
        if (executionData.executionType === '미리보기') {
            modalData.executionResult = {
                maxCount: innerMaxCount,
                fixCount: innerFixCount,
                preCount: innerPreCount,
                preView: innerPreView
            }

            // 미리보기 가능 여부 설정
            if (executionData.executionKafkaOffsetLife === 'Y') {
                modalData.executionResult.preView = 'AVAILABLE'
            } else if (executionData.executionKafkaOffsetLife === 'E') {
                modalData.executionResult.preView = 'EXPIRED'
            } else if (executionData.executionKafkaOffsetLife === 'N') {
                modalData.executionResult.preView = 'NO_DATA'
            }
        } else if (executionData.executionType === '시뮬레이션') {
            // 시뮬레이션 결과 처리 (추후 구현)
            modalData.executionResult = {
                maxCount: 0,
                fixCount: innerFixCount,
                preCount: 0,
                preView: ''
            }
        } else {
            // 기타 실행 타입 (캠페인 대상 생성, 엑셀 데이터 생성 등)
            modalData.executionResult = {
                maxCount: innerMaxCount,
                fixCount: innerFixCount,
                preCount: 0,
                preView: ''
            }
        }

        // 조건 정보 설정
        modalData.targetingCondition = formatConditions(selectTargetCondition)
        modalData.targetingAutoCondition =
            formatAutoConditions(selectTargetOption)
        modalData.targetingReport = formatReportItems(selectTargetItem)

        // 쿼리 정보 설정
        if (executionData.returnCode === 'N000') {
            modalData.executionQuery = formatExecutionQuery(executionData)
        } else {
            modalData.executionQuery = ''
        }

        // 모달 표시
        showResultModal.value = true
    } catch (error) {
        console.error('결과 조회 오류:', error)
        alert('작업 결과를 조회하는 중 오류가 발생했습니다.')
    }
}

/**
 * 타겟팅 조건 포맷팅 (depth 기반 트리 구조)
 * @param {Array} conditions - 타겟팅 조건 배열
 * @returns {String} 포맷팅된 조건 HTML 문자열
 */
function formatConditions(conditions) {
    if (!conditions || conditions.length === 0) {
        return '<p class="text-muted">조건 정보가 없습니다.</p>'
    }

    let html = '<div class="condition-tree">'
    let currentDepth = 1
    let previousDepth = 1

    for (let i = 0; i < conditions.length; i++) {
        const condition = conditions[i]
        currentDepth = condition.conditionDepth || 1

        // AND/OR 연산자 추가 (두 번째 조건부터)
        if (i > 0) {
            const prevCondition = conditions[i - 1]
            const operator = (prevCondition.condition || 'AND').toUpperCase()
            html += `<div class="condition-operator ${operator.toLowerCase()}">${operator}</div>`
        }

        // depth 변경 처리
        if (currentDepth > previousDepth) {
            // depth 증가: 괄호 시작
            const depthDiff = currentDepth - previousDepth
            for (let j = 0; j < depthDiff; j++) {
                html +=
                    '<div class="condition-group depth-' +
                    (previousDepth + j + 1) +
                    '">'
            }
        } else if (currentDepth < previousDepth) {
            // depth 감소: 괄호 종료
            const depthDiff = previousDepth - currentDepth
            for (let j = 0; j < depthDiff; j++) {
                html += '</div>'
            }
        }

        // 조건 항목 렌더링
        const fieldName =
            condition.metaFieldName || condition.fieldName || '조건'
        const operator = formatOperator(condition.operator)
        const value = formatConditionValue(condition)

        html += `
            <div class="condition-item depth-${currentDepth}">
                <span class="condition-field">${fieldName}</span>
                <span class="condition-operator-text">${operator}</span>
                <span class="condition-value">${value}</span>
            </div>
        `

        previousDepth = currentDepth
    }

    // 닫히지 않은 depth 그룹 닫기
    for (let i = currentDepth; i > 1; i--) {
        html += '</div>'
    }

    html += '</div>'
    return html
}

/**
 * 연산자를 한글로 변환
 * @param {String} operator - 연산자
 * @returns {String} 한글 연산자
 */
function formatOperator(operator) {
    const operatorMap = {
        '=': '동등 (=)',
        '< >': '동등하지않음 (< >)',
        '<>': '동등하지않음 (<>)',
        '>': '보다큼 (>)',
        '>=': '크거나 같음 (>=)',
        '<': '보다적음 (<)',
        '<=': '작거나 같음 (<=)',
        IN: '포함 (IN)',
        'NOT IN': '포함하지않음 (NOT IN)',
        "LIKE 'A%'": '시작 (LIKE "A%")',
        "NOT LIKE 'A%'": '시작하지 않음 (NOT LIKE "A%")',
        "LIKE '%A'": '끝 (LIKE "%A")',
        "NOT LIKE '%A'": '끝나지 않음 (NOT LIKE "%A")',
        'IS NULL': '널임 (IS NULL)',
        'IS NOT NULL': '널이아님 (IS NOT NULL)'
    }

    return operatorMap[operator] || operator
}

/**
 * 조건 값 포맷팅
 * @param {Object} condition - 조건 객체
 * @returns {String} 포맷팅된 값
 */
function formatConditionValue(condition) {
    const inputType = condition.inputType
    const operator = condition.operator
    const value = condition.value
    const bidwDimensionYn = condition.bidwMetaDimensionYn

    // IS NULL, IS NOT NULL인 경우 값 없음
    if (operator === 'IS NULL' || operator === 'IS NOT NULL') {
        return ''
    }

    // BIDW 디멘션인 경우
    if (bidwDimensionYn === 'Y') {
        if (inputType === '3') {
            return condition.valueBidwDimenion || value || ''
        }
    }

    // 날짜 함수인 경우 (PostgreSQL 형식)
    // PostgreSQL: CURRENT_DATE + INTERVAL '7 days'
    // PostgreSQL: CURRENT_DATE - INTERVAL '3 days'
    // PostgreSQL: TO_CHAR(CURRENT_DATE, 'YYYYMMDD')
    if (inputType === '2' && value) {
        // PostgreSQL 날짜 함수 형식 체크
        if (
            value.indexOf('CURRENT_DATE') > -1 ||
            value.indexOf('INTERVAL') > -1 ||
            value.indexOf('TO_CHAR') > -1 ||
            value.indexOf('NOW()') > -1 ||
            value.indexOf('CURRENT_TIMESTAMP') > -1
        ) {
            return value
        }
    }

    return value || ''
}

/**
 * 타겟팅 필수 조건 포맷팅
 * @param {Array} options - 타겟팅 옵션 배열
 * @returns {String} 포맷팅된 옵션 HTML 문자열
 */
function formatAutoConditions(options) {
    if (!options || options.length === 0) {
        return '<p class="text-muted">필수 조건이 없습니다.</p>'
    }

    let html = '<div class="auto-conditions">'

    options.forEach((option) => {
        const targetName =
            option.targetName ||
            option.metaFieldName ||
            option.fieldName ||
            '필수조건'
        html += `
            <div class="auto-condition-item">
                <i class="ti ti-checkbox-circle text-primary me-2"></i>
                <span>${targetName}</span>
            </div>
        `
    })

    html += '</div>'
    return html
}

/**
 * 출력 조건 포맷팅
 * @param {Array} items - 출력 항목 배열
 * @returns {String} 포맷팅된 항목 HTML 문자열
 */
function formatReportItems(items) {
    if (!items || items.length === 0) {
        return '<p class="text-muted">출력 조건이 없습니다.</p>'
    }

    let html = '<div class="report-items d-flex flex-wrap gap-2">'

    items.forEach((item) => {
        const fieldName = item.metaFieldName || item.fieldName || '출력항목'
        const functionId = item.targetFunctionId
        const hasFunction = functionId && functionId.trim() !== ''

        // 함수가 있는 경우와 없는 경우 다른 스타일 적용
        const badgeClass = hasFunction
            ? 'badge bg-light-primary text-primary border border-primary'
            : 'badge bg-light text-dark'

        html += `
            <span class="${badgeClass} px-3 py-2">
                ${fieldName}
                ${hasFunction ? '<i class="ti ti-function ms-1"></i>' : ''}
            </span>
        `
    })

    html += '</div>'
    return html
}

/**
 * 실행 쿼리 포맷팅
 * @param {Object} executionData - 실행 결과 데이터
 * @returns {String} 포맷팅된 쿼리 문자열
 */
function formatExecutionQuery(executionData) {
    if (!executionData) {
        return ''
    }

    // returnCode가 N000이 아니면 쿼리 없음
    if (executionData.returnCode !== 'N000') {
        return ''
    }

    const querySelect = executionData.querySelect
    const queryFrom = executionData.queryFrom
    const queryWhere = executionData.queryWhere

    // 쿼리 구성 요소가 없으면 executionQuery 그대로 사용
    if (!querySelect && !queryFrom && !queryWhere) {
        if (executionData.executionQuery) {
            return formatSimpleQuery(executionData.executionQuery)
        }
        return ''
    }

    // 쿼리 조립 및 포맷팅
    return buildFormattedQuery(querySelect, queryFrom, queryWhere)
}

/**
 * 단순 쿼리 포맷팅 (구조 분해가 없는 경우)
 * @param {String} query - 쿼리 문자열
 * @returns {String} 포맷팅된 HTML
 */
function formatSimpleQuery(query) {
    const formattedQuery = highlightSQLKeywords(query)
    return `<div><pre style="font-size: 12px;">${formattedQuery}</pre></div>`
}

/**
 * 구조화된 쿼리 빌드 및 포맷팅
 * @param {Array} querySelect - SELECT 절 배열
 * @param {String} queryFrom - FROM 절 문자열
 * @param {String} queryWhere - WHERE 절 문자열
 * @returns {String} 포맷팅된 HTML
 */
function buildFormattedQuery(querySelect, queryFrom, queryWhere) {
    let queryHtml = ''

    // SELECT 절 처리
    if (querySelect && querySelect.length > 0) {
        queryHtml += 'select ' + querySelect[0]

        for (let i = 1; i < querySelect.length; i++) {
            queryHtml += '\n     , ' + querySelect[i]
        }
    } else {
        queryHtml += 'select *'
    }

    // FROM 절 처리 (left join과 on 키워드 줄바꿈)
    if (queryFrom) {
        let formattedFrom = queryFrom
            .replace(/ left join /gi, '\n       left join ')
            .replace(/ on /gi, '\n              on ')
        queryHtml += '\n  from ' + formattedFrom
    }

    // WHERE 절 처리 (and와 or 키워드 줄바꿈)
    if (queryWhere) {
        let formattedWhere = queryWhere
            .replace(/ and /gi, '\n   and ')
            .replace(/ or /gi, '\n    or ')
        queryHtml += '\n where ' + formattedWhere.trim()
    }

    // SQL 키워드 색상 강조
    const coloredQuery = highlightSQLKeywords(queryHtml)

    return `<div><pre style="font-size: 12px;">${coloredQuery}</pre></div>`
}

/**
 * SQL 키워드에 색상 적용
 * @param {String} query - 원본 쿼리
 * @returns {String} 색상이 적용된 쿼리
 */
function highlightSQLKeywords(query) {
    const cmdColor = 'red'

    return query
        .replace(/select /gi, `<font color="${cmdColor}">select </font>`)
        .replace(/ from /gi, ` <font color="${cmdColor}">from </font>`)
        .replace(/ where /gi, ` <font color="${cmdColor}">where </font>`)
        .replace(/ and /gi, ` <font color="${cmdColor}">and </font>`)
        .replace(/ or /gi, ` <font color="${cmdColor}">or </font>`)
        .replace(/ left join /gi, ` <font color="${cmdColor}">left join </font>`)
        .replace(/ right join /gi, ` <font color="${cmdColor}">right join </font>`)
        .replace(/ inner join /gi, ` <font color="${cmdColor}">inner join </font>`)
        .replace(/ outer join /gi, ` <font color="${cmdColor}">outer join </font>`)
        .replace(/ on /gi, ` <font color="${cmdColor}">on </font>`)
        .replace(/ in /gi, ` <font color="${cmdColor}">in </font>`)
        .replace(/ like /gi, ` <font color="${cmdColor}">like </font>`)
        .replace(/ between /gi, ` <font color="${cmdColor}">between </font>`)
        .replace(/ is null/gi, ` <font color="${cmdColor}">is null</font>`)
        .replace(/ is not null/gi, ` <font color="${cmdColor}">is not null</font>`)
        .replace(/ order by /gi, ` <font color="${cmdColor}">order by </font>`)
        .replace(/ group by /gi, ` <font color="${cmdColor}">group by </font>`)
        .replace(/ having /gi, ` <font color="${cmdColor}">having </font>`)
        .replace(/ limit /gi, ` <font color="${cmdColor}">limit </font>`)
}
</script>
