<template>
    <PageHeader title="데이터 조회" parent="시스템관리" grandParent="관리자" />

    <section class="admin-wrapper data-lockup">
        <b-row class="justify-content-center">
            <b-col xxl="9">
                <b-card class="data-mail-card" no-body>
                    <b-row class="row-cols-1">
                        <b-col>
                            <div class="card-header">
                                <b-button
                                    variant="primary"
                                    size="lg"
                                    @click="generateMail('send')"
                                >
                                    <i class="ti ti-mail-code"></i>
                                    금일 발송 캠페인 메일 생성
                                </b-button>

                                <b-button
                                    variant="info"
                                    size="lg"
                                    @click="generateMail('plan')"
                                >
                                    <i class="ti ti-mail-code"></i>
                                    금일 기획 캠페인 메일 생성
                                </b-button>

                                <b-button
                                    variant="link"
                                    class="ms-auto"
                                    @click="resetMonitoring"
                                >
                                    <i class="ti ti-refresh"></i>
                                    모니터링 초기화
                                </b-button>
                            </div>
                        </b-col>
                        <b-col>
                            <div class="card-body p-4">
                                <!-- =====================
                                    메일 BODY (Simplebar)
                                ====================== -->
                                <h3 v-if="mailType" class="text-center mb-4">
                                    금일
                                    {{ mailType === 'send' ? '발송' : '기획' }}
                                    캠페인 메일
                                </h3>

                                <Simplebar class="mail-preview">
                                    <!-- 초기 안내 -->
                                    <EmptyMessage
                                        v-if="!mailHtml"
                                        class="text-center"
                                    >
                                        하단 버튼을 클릭하면<br />
                                        메일 발송용 HTML 내용이 생성됩니다.
                                    </EmptyMessage>

                                    <!-- 메일 미리보기 -->
                                    <div
                                        v-else
                                        class="mail-body"
                                        v-html="mailHtml"
                                    />
                                </Simplebar>
                            </div>
                        </b-col>
                    </b-row>
                </b-card>
            </b-col>
        </b-row>
    </section>
</template>

<script setup>
import { ref } from 'vue'
import Simplebar from 'simplebar-vue'
import PageHeader from '@/components/PageHeader.vue'
import EmptyMessage from '@/components/EmptyMessage.vue'
import Swal from 'sweetalert2'

/* =====================
   state
===================== */
const mailHtml = ref('')
const mailType = ref('')

/* =====================
   메일 생성
===================== */
const generateMail = async (type) => {
    mailType.value = type
    const label = type === 'send' ? '발송' : '기획'

    const html = `
        <div style="font-family: Pretendard, Arial, sans-serif; line-height: 1.6;">
            <p>안녕하세요. MVNO 홍길동입니다.</p>
            <p>오후 모니터링 보고드립니다.</p>

            <h5>1. 정기 캠페인 ${label} 대상: 총 <strong>*건</strong></h5>
            ${createTable(type)}

            <h5>2. 메시지 캠페인 ${label} 대상: 총 <strong>*건</strong></h5>
            ${createTable(type)}

            <h5>3. 앱푸시 캠페인 ${label} 대상: 총 <strong>*건</strong></h5>
            ${createTable(type)}

            <p style="margin-top: 24px;">감사합니다.</p>
        </div>
    `

    mailHtml.value = html

    /* ✅ 클립보드 복사 */
    try {
        await navigator.clipboard.writeText(html)

        Swal.fire({
            icon: 'success',
            title: '메일 생성 완료',
            html: `
                <b>${label} 캠페인 메일</b>이 생성되었고<br/>
                클립보드에 복사되었습니다.
            `,
            timer: 2000,
            showConfirmButton: false
        })
    } catch (e) {
        Swal.fire('복사 실패', '클립보드 복사에 실패했습니다.', 'error')
    }
}

/* =====================
   테이블 HTML 생성
===================== */
const createTable = (type) => {
    // ✅ 발송 테이블
    if (type === 'send') {
        return `
            <table border="1" cellpadding="6" cellspacing="0" width="100%"
                style="border-collapse: collapse; border-color: #ddd; margin-bottom: 20px;">
                <thead style="background:#f5f6fa;">
                    <tr>
                        <th>No</th>
                        <th>캠페인명</th>
                        <th>메시지아이디</th>
                        <th>발송예정시간</th>
                        <th>nMIMO전송시간</th>
                        <th>발송상태</th>
                        <th>편성건수</th>
                        <th>대상</th>
                        <th>수신률</th>
                        <th>비고</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td colspan="10" style="text-align:center; color:#999;">
                            데이터 없음
                        </td>
                    </tr>
                </tbody>
            </table>
        `
    }

    // ✅ 기획 테이블
    return `
        <table border="1" cellpadding="6" cellspacing="0" width="100%"
            style="border-collapse: collapse; border-color: #ddd; margin-bottom: 20px;">
            <thead style="background:#f5f6fa;">
                <tr>
                    <th>No</th>
                    <th>캠페인명</th>
                    <th>메시지아이디</th>
                    <th>수행주기</th>
                    <th>발송상태</th>
                    <th>대상</th>
                    <th>비고</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td colspan="7" style="text-align:center; color:#999;">
                        데이터 없음
                    </td>
                </tr>
            </tbody>
        </table>
    `
}

/* =====================
   초기화
===================== */
const resetMonitoring = () => {
    Swal.fire({
        title: '모니터링 초기화',
        text: '모니터링 데이터를 초기화하시겠습니까?',
        icon: 'warning',
        showCancelButton: true
    }).then((res) => {
        if (res.isConfirmed) {
            mailHtml.value = ''
            mailType.value = ''
        }
    })
}
</script>
