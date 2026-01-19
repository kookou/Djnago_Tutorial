<template>
    <PageHeader title="권한 관리" parent="시스템관리" grandParent="관리자" />

    <div class="admin-wrapper">
        <div class="admin-content">
            <section>
                <b-card header-class="d-flex align-items-center">
                    <template #header>
                        <h5 class="card-title mb-0">
                            권한 목록
                            <span class="text-info ms-1">3</span>
                        </h5>
                        <b-button
                            variant="light-2"
                            class="ms-auto"
                            @click="openCreateModal"
                        >
                            <i class="ti ti-plus"></i> 권한 추가
                        </b-button>
                    </template>

                    <Simplebar :style="{ height: contentHeight + 'px' }">
                        <b-row
                            class="row-cols-1 row-cols-lg-2 row-cols-xl-3 g-3 mx-0"
                        >
                            <b-col v-for="(role, index) in roles" :key="index">
                                <b-card class="border mb-0" body-class="p-3">
                                    <b-row class="g-3">
                                        <b-col cols="auto">
                                            <div class="avatar-sm">
                                                <div
                                                    class="avatar-title bg-primary-subtle text-body rounded-circle fs-20"
                                                >
                                                    {{ role.roleNm.charAt(0) }}
                                                </div>
                                            </div>
                                        </b-col>

                                        <b-col>
                                            <h5 class="my-1">
                                                {{ role.roleNm }}
                                                <span class="ms-2 text-primary">
                                                    {{ role.roleCd }}
                                                </span>
                                            </h5>
                                            <p class="mb-0 text-muted">
                                                {{ role.period }}
                                            </p>
                                        </b-col>

                                        <b-col sm="auto" class="d-flex gap-1">
                                            <b-button
                                                variant="link"
                                                class="btn-icon"
                                                size="sm"
                                                @click="
                                                    openEditModal(role, index)
                                                "
                                            >
                                                <i class="ti ti-edit"></i>
                                            </b-button>

                                            <b-button
                                                variant="link"
                                                class="btn-icon"
                                                size="sm"
                                                @click="deleteRole(index)"
                                            >
                                                <i class="ti ti-trash"></i>
                                            </b-button>
                                        </b-col>
                                    </b-row>
                                </b-card>
                            </b-col>
                        </b-row>
                    </Simplebar>
                </b-card>
            </section>
        </div>
    </div>

    <!-- Modal: 권한 추가 / 수정 -->
    <RoleCreateModal
        v-model="showCreateModal"
        :edit-data="editRoleData"
        @saved="onRoleSaved"
    />
</template>
<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import PageHeader from '@/components/PageHeader'
import Simplebar from 'simplebar-vue'
import Swal from 'sweetalert2'
import RoleCreateModal from '@/components/admin/system/RoleCreateModal.vue'

/* =========================
   권한 목록 (초기 데이터)
========================= */
const roles = ref([
    {
        roleNm: '관리자',
        roleCd: 'RD0001',
        period: '2025-01-01 ~ 2026-12-31'
    },
    {
        roleNm: '일반관리자',
        roleCd: 'RD0002',
        period: '2025-01-01 ~ 2026-12-31'
    },
    {
        roleNm: '시스템관리자',
        roleCd: 'RD0003',
        period: '2025-01-01 ~ 2026-12-31'
    }
])

/* =========================
   모달 상태
========================= */
const showCreateModal = ref(false)
const editRoleData = ref(null)
const editIndex = ref(null)

/* =========================
   추가 모달
========================= */
const openCreateModal = () => {
    editRoleData.value = null
    editIndex.value = null
    showCreateModal.value = true
}

/* =========================
   수정 모달
========================= */
const openEditModal = (role, index) => {
    editRoleData.value = { ...role }
    editIndex.value = index
    showCreateModal.value = true
}

/* =========================
   저장 (추가 / 수정 공통)
========================= */
const onRoleSaved = (role) => {
    if (editIndex.value !== null) {
        // 수정
        roles.value.splice(editIndex.value, 1, role)
    } else {
        // 추가
        roles.value.push(role)
    }

    showCreateModal.value = false
    editRoleData.value = null
    editIndex.value = null
}

/* =========================
   삭제
========================= */
const deleteRole = async (index) => {
    const role = roles.value[index]

    const result = await Swal.fire({
        title: '권한 삭제',
        html: `
        <p class=" text-danger">다음 권한을 삭제하시겠습니까?</p>
            <div class="text-body fw-semibold">${role.roleNm}<span class="ms-1 text-primary">(${role.roleCd})</span></strong>
        `,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '삭제',
        cancelButtonText: '취소',
        confirmButtonColor: '#f1416c',
        cancelButtonColor: '#e4e6ef',
        reverseButtons: true
    })

    if (!result.isConfirmed) return

    roles.value.splice(index, 1)

    Swal.fire({
        toast: true,
        position: 'top-end',
        icon: 'success',
        title: '권한이 삭제되었습니다',
        showConfirmButton: false,
        timer: 1500
    })
}

/* =========================
   높이 계산
========================= */
const contentHeight = ref(400)
const HEADER_OFFSET = 200

const calcHeight = () => {
    contentHeight.value = window.innerHeight - HEADER_OFFSET
}

onMounted(() => {
    calcHeight()
    window.addEventListener('resize', calcHeight)
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', calcHeight)
})
</script>
