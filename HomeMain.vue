<template>
    <div class="home-wrapper">
        <section class="home-target-group">
            <div class="container">
                <div class="text-center">
                    <h3 class="mb-1 fs-22">
                        <span class="text-primary">MVNO CRM</span>은 캠페인을
                        수행하기 위한<br />모수를 타겟팅할 수 있는 서비스입니다.
                    </h3>
                    <p class="text-muted fs-13 mb-0">
                        목적에 맞는 주제영역(데이터)을 선택하기 위한 작업 유형을
                        아래에서 선택해주세요.
                    </p>
                </div>

                <TargetGroupSelector
                    v-model="selectedPurposeObj"
                    :target-area-group="targetAreaGroup"
                    :cols="{ cols: 6, sm: 4, md: 3, lg: 2, xl: 2 }"
                    @select="onSelectGroup"
                />
            </div>
        </section>

        <section class="home-content">
            <div class="container">
                <b-row class="g-3">
                    <!-- 내 타겟 작업 모아보기 / AI 추천 -->
                    <b-col cols="12" lg="9">
                        <b-card no-body class="h-100">
                            <b-tabs
                                v-model="activeTab"
                                card
                                nav-class="nav-tabs-custom border-bottom-0"
                            >
                                <!-- 1️⃣ 내 타겟 작업 모아보기 -->
                                <b-tab
                                    title="내 타겟 작업 모아보기"
                                    name="target"
                                    active
                                >
                                    <b-row
                                        class="table-header align-items-center mb-2"
                                    >
                                        <b-col sm="auto">
                                            <p class="mb-0 text-muted">
                                                최근 작업한
                                                <strong class="text-dark">{{
                                                    targetWorkList.length
                                                }}</strong
                                                >개의 타겟 작업 목록입니다.
                                            </p>
                                        </b-col>
                                        <b-col sm="auto" class="ms-auto">
                                            <b-form-checkbox
                                                switch
                                                v-model="includeSimulation"
                                                >시뮬레이션
                                                포함</b-form-checkbox
                                            >
                                        </b-col>
                                    </b-row>

                                    <Simplebar>
                                        <b-table
                                            :items="targetWorkList"
                                            :fields="targetWorkFields"
                                            small
                                            striped
                                            hover
                                            head-variant="light"
                                            class="align-middle text-center table-nowrap"
                                        >
                                            <!-- 워크북명 + badge -->
                                            <template #cell(workbook)="data">
                                                <b-badge
                                                    variant="info-subtle"
                                                    class="bg-info-subtle text-info me-1"
                                                    >{{
                                                        data.item.workbookType
                                                    }}</b-badge
                                                >
                                                {{ data.item.workbook }}
                                            </template>

                                            <!-- 작업상태 -->
                                            <template #cell(status)="data">
                                                <b-badge
                                                    :variant="
                                                        getStatusStyle(
                                                            data.item.status
                                                        ).variant
                                                    "
                                                    :class="[
                                                        getStatusStyle(
                                                            data.item.status
                                                        ).class
                                                    ]"
                                                >
                                                    {{ data.item.status }}
                                                </b-badge>
                                            </template>

                                            <!-- 상세보기 버튼 -->
                                            <template #cell(view)="data">
                                                <a
                                                    href="#"
                                                    class="fs-12 text-info"
                                                    >더 보기
                                                    <i
                                                        class="ti ti-arrow-right fs-13 align-middle"
                                                    ></i
                                                ></a>
                                            </template>
                                        </b-table>
                                    </Simplebar>
                                </b-tab>

                                <!-- 2️⃣ AI 기반 추천 캠페인 -->
                                <b-tab title="AI 기반 추천 캠페인" name="ai">
                                    <b-row
                                        class="table-header align-items-center mb-2"
                                    >
                                        <b-col>
                                            <p class="mb-0 text-muted">
                                                AI 학습을 통한 추천 캠페인(타겟)
                                                목록입니다.
                                            </p>
                                        </b-col>
                                    </b-row>

                                    <Simplebar>
                                        <b-table
                                            :items="aiRecommendList"
                                            :fields="aiRecommendFields"
                                            small
                                            striped
                                            hover
                                            bordered
                                            head-variant="light"
                                            class="align-middle text-center table-nowrap"
                                            :tbody-tr-class="rowClass"
                                            @row-toggled="onRowToggled"
                                            @row-clicked="onRowClicked"
                                        >
                                            <!-- + 버튼 -->
                                            <template #cell(toggle)="row">
                                                <b-button
                                                    size="sm"
                                                    variant="link"
                                                    class="p-0"
                                                    @click.stop="
                                                        toggleRow(row.item)
                                                    "
                                                >
                                                    <i
                                                        :class="
                                                            expandedRowId ===
                                                            row.item.id
                                                                ? 'ti ti-chevron-down text-primary'
                                                                : 'ti ti-chevron-right'
                                                        "
                                                    ></i>
                                                </b-button>
                                            </template>

                                            <!-- 캠페인명 + 추천 아이콘 -->
                                            <template #cell(campaign)="data">
                                                <span
                                                    class="d-inline-flex align-items-center gap-1"
                                                >
                                                    <i
                                                        v-if="data.item.rank"
                                                        class="ti ti-sparkles"
                                                        :class="
                                                            getMedalColor(
                                                                data.item.rank
                                                            )
                                                        "
                                                        title="AI 추천 상위 캠페인"
                                                    ></i>
                                                    {{ data.item.campaign }}
                                                </span>
                                            </template>

                                            <!-- Row Details -->
                                            <template #row-details="row">
                                                <div class="details-table">
                                                    <b-table
                                                        :items="
                                                            row.item.details
                                                        "
                                                        :fields="
                                                            aiRecommendDetailFields
                                                        "
                                                        small
                                                        head-variant="light"
                                                        class="align-middle text-center mb-0"
                                                    >
                                                        <template
                                                            #cell(load)="data"
                                                        >
                                                            <b-button
                                                                size="sm"
                                                                variant="light-2"
                                                                >로드하기</b-button
                                                            >
                                                        </template>
                                                    </b-table>
                                                </div>
                                            </template>
                                            <!-- ✅ Row Details -->
                                        </b-table>
                                    </Simplebar>
                                </b-tab>
                            </b-tabs>
                        </b-card>
                    </b-col>

                    <!-- 내 워크북 바로가기 -->
                    <b-col cols="12" lg="3">
                        <b-card class="my-workbook h-100">
                            <template #header>
                                <h5 class="card-title mb-0">
                                    내 워크북 바로가기
                                </h5>
                            </template>

                            <Simplebar>
                                <b-card
                                    v-for="(item, i) in workbookList"
                                    :key="i"
                                    class="my-workbook-item card-animate"
                                >
                                    <div
                                        class="hstack gap-1 justify-content-between"
                                    >
                                        <h5 class="mb-0">
                                            {{ item.name }}
                                        </h5>
                                        <i
                                            class="ti ti-folder-filled fs-18 text-primary opacity-50"
                                        ></i>
                                    </div>
                                    <small class="text-muted">
                                        마지막 수정 시간: 2025-10-22 13:45:00
                                    </small>
                                    <p class="mb-0 text-muted">
                                        타겟작업
                                        <strong class="text-primary">{{
                                            item.count
                                        }}</strong
                                        >개
                                    </p>
                                </b-card>
                            </Simplebar>
                        </b-card>
                    </b-col>

                    <!-- 공지사항 -->
                    <b-col>
                        <b-card class="notice-wrapper">
                            <template #header>
                                <h5 class="card-title mb-0">공지사항</h5>
                            </template>
                            <b-row class="g-2">
                                <!-- 공지사항 리스트 -->
                                <b-col cols="12" lg="6">
                                    <b-card class="notice-list">
                                        <b-row class="table-header">
                                            <b-col sm="auto" class="status">
                                                <h5>
                                                    전체
                                                    <span>{{ total }}</span
                                                    >건
                                                </h5>
                                            </b-col>
                                        </b-row>
                                        <Simplebar>
                                            <b-table
                                                :items="sortedNoticeList"
                                                :fields="noticeFields"
                                                hover
                                                small
                                                striped
                                                head-variant="light"
                                                class="align-middle text-center table-nowrap"
                                                @row-clicked="
                                                    (item) =>
                                                        (selectedNotice = item)
                                                "
                                                :tbody-tr-class="rowClassNotice"
                                            >
                                                <!-- 제목 클릭 시 강조 -->
                                                <template #cell(title)="data">
                                                    <span
                                                        class="fw-semibold"
                                                        role="button"
                                                        @click.stop="
                                                            selectedNotice =
                                                                data.item
                                                        "
                                                    >
                                                        {{ data.item.title }}
                                                    </span>
                                                </template>

                                                <!-- 작성일자 포맷 -->
                                                <template #cell(date)="data">
                                                    {{
                                                        new Date(
                                                            data.item.date
                                                        ).toLocaleString()
                                                    }}
                                                </template>
                                            </b-table>
                                        </Simplebar>
                                    </b-card>
                                </b-col>

                                <!-- 공지사항 본문 -->
                                <b-col cols="12" lg="6">
                                    <b-card class="notice-content">
                                        <div v-if="selectedNotice">
                                            <div class="notice-header">
                                                <h3>
                                                    {{ selectedNotice.title }}
                                                </h3>
                                                <div
                                                    class="hstack gap-3 flex-wrap"
                                                >
                                                    <p class="text-muted mb-0">
                                                        작성자:
                                                        {{
                                                            selectedNotice.author
                                                        }}
                                                    </p>
                                                    <div class="vr my-1"></div>
                                                    <p class="text-muted mb-0">
                                                        작성일:
                                                        {{
                                                            new Date(
                                                                selectedNotice.date
                                                            ).toLocaleString()
                                                        }}
                                                    </p>
                                                </div>
                                            </div>
                                            <Simplebar>
                                                <p>
                                                    {{ selectedNotice.content }}
                                                </p>
                                            </Simplebar>
                                        </div>

                                        <div
                                            v-else
                                            class="text-muted text-center p-4"
                                        >
                                            공지사항을 선택해주세요.
                                        </div>
                                    </b-card>
                                </b-col>
                            </b-row>
                        </b-card>
                    </b-col>
                </b-row>
            </div>
        </section>
    </div>
</template>
<script setup>
import { ref, onMounted, nextTick, computed } from 'vue'
import { useRouter } from 'vue-router'
import TargetGroupSelector from '@/components/expert/TargetGroupSelector.vue'
import Simplebar from 'simplebar-vue'
import * as expertModules from '@/modules/expert'
import { useExpertStore } from '@/store/expert'

const router = useRouter()
const selectedPurposeObj = ref(null)
const targetAreaGroup = ref([])

const activeTab = ref('target')
const includeSimulation = ref(false)

// [내 타겟 작업 목록]
const targetWorkFields = [
    { key: 'id', label: '번호', thStyle: { width: '50px' } },
    { key: 'date', label: '등록일' },
    { key: 'workbook', label: '워크북명', tdClass: 'text-start' },
    {
        key: 'name',
        label: '타겟 작업명',
        tdAttr: { class: 'text-start text-truncate', style: 'max-width:300px' }
    },
    { key: 'type', label: '작업형태' },
    { key: 'status', label: '작업상태' },
    { key: 'view', label: '상세보기', thStyle: { width: '80px' } }
]
const targetWorkList = ref([
    {
        id: 1,
        date: '2025-10-24 17:55:00',
        workbookType: '개인',
        workbook: '고객세분화',
        name: '고객등급별 타겟 작업',
        type: '대상확정',
        status: '편성완료'
    },
    {
        id: 2,
        date: '2025-10-23 15:40:00',
        workbookType: '개인',
        workbook: '해지방어 캠페인',
        name: '이탈예정자 분석',
        type: '미리보기',
        status: '임시저장'
    }
])

// 상태별 색상 매핑
const statusMap = {
    편성완료: { variant: 'info-subtle', class: 'bg-info-subtle text-info' },
    임시저장: { variant: 'light-subtle', class: 'bg-light-subtle text-muted' },
    시스템오류: { variant: 'danger', class: 'bg-danger-subtle text-danger' },
    진행중: {
        variant: 'primary-subtle',
        class: 'bg-primary-subtle text-primary'
    },
    대기중: { variant: 'warning-subtle', class: 'bg-light-subtle text-body' },
    default: { variant: 'light', class: 'bg-light text-muted' }
}
function getStatusStyle(status) {
    return statusMap[status] || statusMap.default
}

// [AI 캠페인 상위 테이블]
const aiRecommendFields = [
    { key: 'toggle', label: '', thStyle: { width: '30px' } },
    { key: 'department', label: '본부', tdClass: 'text-start' },
    { key: 'campaign', label: '캠페인명', tdClass: 'text-start' },
    { key: 'purpose', label: '캠페인목적', tdClass: 'text-start' },
    { key: 'detailPurpose', label: '캠페인상세목적', tdClass: 'text-start' },
    { key: 'channel', label: '캠페인채널' }
]
const aiRecommendList = ref([
    {
        id: 1,
        department: 'Customer사업본부',
        campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
        purpose: '업셀링',
        detailPurpose: '무선요금제업셀링',
        channel: '메시지캠페인',
        rank: 1,
        details: [
            {
                rank: 1,
                department: 'Customer사업본부',
                campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
                purpose: '업셀링',
                detailPurpose: '무선요금제업셀링',
                channel: '메시지캠페인'
            }
        ]
    },
    {
        id: 2,
        department: 'Customer사업본부',
        campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
        purpose: '업셀링',
        detailPurpose: '무선요금제업셀링',
        channel: '메시지캠페인',
        rank: 2,
        details: [
            {
                rank: 1,
                department: 'Customer사업본부',
                campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
                purpose: '업셀링',
                detailPurpose: '무선요금제업셀링',
                channel: '메시지캠페인'
            }
        ]
    },
    {
        id: 3,
        department: 'Customer사업본부',
        campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
        purpose: '업셀링',
        detailPurpose: '무선요금제업셀링',
        channel: '메시지캠페인',
        rank: 3,
        details: [
            {
                rank: 1,
                department: 'Customer사업본부',
                campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
                purpose: '업셀링',
                detailPurpose: '무선요금제업셀링',
                channel: '메시지캠페인'
            }
        ]
    },
    {
        id: 4,
        department: 'Customer사업본부',
        campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
        purpose: '업셀링',
        detailPurpose: '무선요금제업셀링',
        channel: '메시지캠페인',
        details: [
            {
                rank: 1,
                department: 'Customer사업본부',
                campaign: '(무선사업팀)5G 37K 오퍼링_40대 이하',
                purpose: '업셀링',
                detailPurpose: '무선요금제업셀링',
                channel: '메시지캠페인'
            }
        ]
    }
])

function getMedalColor(rank) {
    switch (rank) {
        case 1:
            return 'text-warning'
        case 2:
            return 'text-dark opacity-50'
        case 3:
            return 'text-bronze'
        default:
            return ''
    }
}

const expandedRowId = ref(null)

// ✅ 행 열기/닫기 (아이콘 또는 행 클릭 공통)
function toggleRow(item) {
    if (expandedRowId.value === item.id) {
        item._showDetails = false
        expandedRowId.value = null
    } else {
        aiRecommendList.value.forEach((r) => (r._showDetails = false))
        item._showDetails = true
        expandedRowId.value = item.id
    }
    // 렌더 후 active 반영
    nextTick(updateActiveRow)
}

// ✅ 행 클릭
function onRowClicked(item) {
    toggleRow(item)
}

// ✅ row-toggled 이벤트 동기화
function onRowToggled(ctx) {
    expandedRowId.value = ctx.expanded ? ctx.item.id : null
    nextTick(updateActiveRow)
}

// ✅ 부모행만 active 처리 (row-details는 제외)
function updateActiveRow() {
    const rows = document.querySelectorAll('.table tbody tr')
    rows.forEach((tr) => tr.classList.remove('active'))

    if (expandedRowId.value !== null) {
        // 상세 행 다음 tr이 아니라, 실제 부모행만 찾기
        const parentRow = Array.from(rows).find((tr) =>
            tr.innerText.includes(
                aiRecommendList.value.find((r) => r.id === expandedRowId.value)
                    ?.campaign
            )
        )
        if (parentRow) parentRow.classList.add('active')
    }
}

// [AI 상세 테이블]
const aiRecommendDetailFields = [
    { key: 'rank', label: '순위', thStyle: { width: '50px' } },
    { key: 'department', label: '본부', tdClass: 'text-start' },
    { key: 'campaign', label: '캠페인명', tdClass: 'text-start' },
    { key: 'purpose', label: '캠페인목적', tdClass: 'text-start' },
    { key: 'detailPurpose', label: '캠페인상세목적', tdClass: 'text-start' },
    { key: 'channel', label: '캠페인채널', tdClass: 'text-start' },
    { key: 'load', label: '타겟팅 로드', thStyle: { width: '100px' } }
]

// 워크북
const workbookList = ref([
    { name: '고객 세분화 워크북', count: 12 },
    { name: '신규가입자 캠페인', count: 8 },
    { name: '유입경로 분석', count: 5 }
])
function goToWorkbook(item) {
    // 워크북 상세 페이지나 메인 페이지로 이동
    router.push({
        name: 'WorkbookMain', // 실제 라우터 네임에 맞게 수정
        query: { name: item.name } // 필요 시 id나 name 전달
    })
}

// 타겟그룹 선택
const store = useExpertStore()
function onSelectGroup(group) {
    if (!group) return
    console.log('선택된 그룹:', group)
    const targetAreaGroupId = group.targetAreaGroupId
    store.setTargetGroupId(targetAreaGroupId)
    router.push({
        name: 'ExpertMain'
    })
}

// 공지사항
const noticeFields = [
    { key: 'id', label: '번호', thStyle: { width: '60px' } },
    { key: 'title', label: '제목', tdClass: 'text-start' },
    { key: 'author', label: '작성자', thStyle: { width: '120px' } },
    { key: 'date', label: '작성일자', thStyle: { width: '180px' } }
]

function rowClassNotice(item) {
    return item.id === selectedNotice.value?.id ? 'active' : ''
}

const noticeList = ref([
    {
        id: 1,
        title: '10월 시스템 점검 안내',
        author: '운영팀',
        date: '2025-10-15T15:10:45',
        content:
            '시스템 안정화를 위한 정기 점검이 10월 20일 00시~02시에 진행됩니다.'
    },
    {
        id: 2,
        title: 'AI 추천 캠페인 기능 오픈',
        author: '기획팀',
        date: '2025-10-22T09:45:00',
        content:
            'AI 추천 캠페인 기능이 새롭게 추가되었습니다. 사용 가이드에서 자세히 확인하세요.'
    },
    {
        id: 3,
        title: '서비스 이용약관 개정 안내',
        author: '관리자',
        date: '2025-10-25T18:20:30',
        content:
            '이용약관이 개정되어 11월 1일부터 시행됩니다. 자세한 내용은 공지사항을 참고하세요.'
    }
])

// 날짜 기준 내림차순 정렬
const sortedNoticeList = computed(() =>
    [...noticeList.value].sort((a, b) => new Date(b.date) - new Date(a.date))
)

// 화면 로드시 최신글 선택
const selectedNotice = ref(null)
onMounted(() => {
    if (sortedNoticeList.value.length > 0) {
        selectedNotice.value = sortedNoticeList.value[0]
    }
})

onMounted(async () => {
    try {
        const res = await expertModules.selectTargetAreaGroup({})
        targetAreaGroup.value = res?.selectTargetAreaGroup || []
    } catch (err) {
        console.warn('타겟 영역 불러오기 실패:', err)
        targetAreaGroup.value = []
    }
})
</script>
