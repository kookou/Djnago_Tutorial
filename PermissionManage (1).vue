<template>
    <PageHeader title="권한 관리" parent="시스템관리" grandParent="관리자" />

    <div class="admin-wrapper permission-manage-wrapper">
        <!-- =====================
             좌측: 권한 목록
        ====================== -->
        <div class="admin-sidebar">
            <b-card header-class="admin-sidebar-header">
                <template #header>
                    <h4 class="mb-0">
                        권한 목록
                        <span class="text-info ms-1">
                            {{ roles.length }}
                        </span>
                    </h4>

                    <b-button
                        variant="link"
                        size="sm"
                        class="btn-icon"
                        @click="openCreateUser"
                    >
                        <i class="ti ti-plus"></i>
                    </b-button>
                </template>

                <Simplebar :style="{ height: leftHeight + 'px' }">
                    <div class="vstack gap-2 pt-1">
                        <b-card
                            v-for="role in roles"
                            :key="role.roleCd"
                            class="card-animate role-item"
                            :class="{
                                active: selectedRole?.roleCd === role.roleCd
                            }"
                            @click="selectRole(role)"
                        >
                            <div class="d-flex align-items-center gap-2">
                                <div class="flex-shrink-0">
                                    <div class="avatar-sm">
                                        <div
                                            class="avatar-title bg-primary-subtle text-body rounded-circle fs-20"
                                        >
                                            {{ role.roleNm.charAt(0) }}
                                        </div>
                                    </div>
                                </div>

                                <div class="flex-grow-1">
                                    <h5 class="mb-1">
                                        {{ role.roleNm }}
                                        <span class="ms-2 text-primary">
                                            {{ role.roleCd }}
                                        </span>
                                    </h5>
                                    <p class="mb-0 text-muted">
                                        {{
                                            formatPeriod(
                                                role.startDate,
                                                role.endDate
                                            )
                                        }}
                                    </p>
                                </div>
                            </div>
                        </b-card>
                    </div>
                </Simplebar>
            </b-card>
        </div>

        <!-- =====================
             우측: 권한 상세 / 편집
        ====================== -->
        <div class="admin-content">
            <b-card>
                <template #header>
                    <h4 class="mb-0">
                        <template v-if="selectedRole">
                            <span class="text-muted fw-normal"
                                >권한 정보 :</span
                            >
                            <span class="ms-1">{{ form.roleNm }}</span>
                            <span class="text-primary ms-2">{{
                                form.roleCd
                            }}</span>
                        </template>
                        <template v-else>
                            <span class="text-muted fw-normal">
                                <i class="ti ti-info-circle"></i>
                                권한을 선택하세요.
                            </span>
                        </template>
                    </h4>
                </template>

                <Simplebar :style="{ height: rightScrollHeight + 'px' }">
                    <div v-if="selectedRole">
                        <b-row class="g-4 mx-0">
                            <!-- 기본 설정 -->
                            <b-col xl="6">
                                <h5 class="text-muted">기본 설정</h5>
                                <div class="edit-box py-3">
                                    <b-row class="row-cols-1 g-3">
                                        <b-col>
                                            <label class="form-label required"
                                                >권한명</label
                                            >
                                            <b-form-input
                                                v-model="form.roleNm"
                                                :class="{
                                                    'is-modified':
                                                        isModified('roleNm')
                                                }"
                                            />
                                        </b-col>

                                        <b-col>
                                            <label class="form-label required"
                                                >권한 코드</label
                                            >
                                            <b-form-input
                                                v-model="form.roleCd"
                                                disabled
                                            />
                                        </b-col>

                                        <b-col>
                                            <label class="form-label"
                                                >유효 기간</label
                                            >
                                            <div class="hstack gap-1">
                                                <flat-pickr
                                                    v-model="form.startDate"
                                                    :config="dayPickerConfig"
                                                    class="form-control"
                                                    placeholder="시작일"
                                                />
                                                <span>~</span>
                                                <flat-pickr
                                                    v-model="form.endDate"
                                                    :config="dayPickerConfig"
                                                    class="form-control"
                                                    placeholder="종료일"
                                                />
                                            </div>
                                        </b-col>
                                    </b-row>
                                </div>
                            </b-col>

                            <!-- 메뉴 설정 -->
                            <b-col xl="6">
                                <h5 class="text-muted">메뉴 설정</h5>

                                <div class="menu-tree edit-box py-3">
                                    <Simplebar
                                        :style="{
                                            height: contentHeight + 'px'
                                        }"
                                    >
                                        <div
                                            v-for="menu in menuTree"
                                            :key="menu.id"
                                            class="tree-node"
                                        >
                                            <!-- 부모 -->
                                            <div class="tree-item tree-parent">
                                                <label>
                                                    <input
                                                        type="checkbox"
                                                        class="form-check-input"
                                                        :checked="
                                                            isChecked(menu.id)
                                                        "
                                                        @change="
                                                            toggleParent(menu)
                                                        "
                                                    />
                                                    {{ menu.name }}
                                                </label>
                                            </div>

                                            <!-- 자식 -->
                                            <div class="tree-children">
                                                <div
                                                    v-for="child in menu.children"
                                                    :key="child.id"
                                                    class="tree-item tree-child"
                                                >
                                                    <label>
                                                        <input
                                                            type="checkbox"
                                                            class="form-check-input"
                                                            :checked="
                                                                isChecked(
                                                                    child.id
                                                                )
                                                            "
                                                            @change="
                                                                toggleChild(
                                                                    menu,
                                                                    child
                                                                )
                                                            "
                                                        />
                                                        {{ child.name }}
                                                    </label>
                                                </div>
                                            </div>
                                        </div>
                                    </Simplebar>
                                </div>
                            </b-col>
                        </b-row>
                    </div>

                    <EmptyMessage v-else>
                        권한 목록에서 항목을 선택하세요.
                    </EmptyMessage>
                </Simplebar>

                <template #footer>
                    <div class="btn-area" v-if="selectedRole">
                        <b-button
                            v-if="!isCreateMode"
                            variant="soft-danger"
                            class="me-auto"
                            @click="deleteRole"
                        >
                            삭제
                        </b-button>
                        <b-button
                            variant="light"
                            :disabled="!isDirty"
                            @click="cancelEdit"
                            class="ms-auto"
                        >
                            취소
                        </b-button>

                        <b-button
                            v-if="!isCreateMode"
                            variant="soft-primary"
                            @click="duplicateRole"
                        >
                            복제
                        </b-button>

                        <b-button
                            variant="dark"
                            :disabled="!isDirty"
                            @click="saveRole"
                        >
                            저장
                        </b-button>
                    </div>
                </template>
            </b-card>
        </div>
    </div>
</template>
<script setup>
import { ref, watch, onMounted, onBeforeUnmount } from 'vue'
import PageHeader from '@/components/PageHeader'
import Simplebar from 'simplebar-vue'
import Swal from 'sweetalert2'
import flatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import EmptyMessage from '@/components/EmptyMessage.vue'

/* =========================
   상태
========================= */
const isCreateMode = ref(false)
const selectedRole = ref(null)
const form = ref({})
const original = ref({})
const isDirty = ref(false)

/* =========================
   권한 목록
========================= */
const roles = ref([
    {
        roleNm: '관리자',
        roleCd: 'RD0001',
        startDate: '2025-01-01',
        endDate: '2026-12-31',
        menus: ['SYSTEM', 'SYSTEM_ROLE']
    },
    {
        roleNm: '일반관리자',
        roleCd: 'RD0002',
        startDate: '2025-01-01',
        endDate: '2026-12-31',
        menus: ['CAMPAIGN', 'CAMPAIGN_LIST']
    }
])

/* =========================
   목록 표시용 기간
========================= */
const formatPeriod = (start, end) => {
    if (!start || !end) return '-'
    return `${start} ~ ${end}`
}

/* =========================
   메뉴 트리
========================= */
const menuTree = [
    {
        id: 'SYSTEM',
        name: '시스템 관리',
        children: [
            { id: 'SYSTEM_USER', name: '사용자 관리' },
            { id: 'SYSTEM_ROLE', name: '권한 관리' }
        ]
    },
    {
        id: 'CAMPAIGN',
        name: '캠페인 관리',
        children: [
            { id: 'CAMPAIGN_LIST', name: '캠페인 목록' },
            { id: 'CAMPAIGN_RESULT', name: '캠페인 결과' }
        ]
    }
]

const isChecked = (id) =>
    Array.isArray(form.value.menus) && form.value.menus.includes(id)

const toggleMenu = (id) => {
    const idx = form.value.menus.indexOf(id)
    if (idx > -1) {
        form.value.menus.splice(idx, 1)
    } else {
        form.value.menus.push(id)
    }
}

const toggleParent = (menu) => {
    const childIds = menu.children.map((c) => c.id)
    const hasAllChildren = childIds.every((id) => form.value.menus.includes(id))

    if (hasAllChildren) {
        // 전체 해제
        form.value.menus = form.value.menus.filter(
            (id) => id !== menu.id && !childIds.includes(id)
        )
    } else {
        // 전체 선택
        form.value.menus = Array.from(
            new Set([...form.value.menus, menu.id, ...childIds])
        )
    }
}
const toggleChild = (menu, child) => {
    toggleMenu(child.id)

    const childIds = menu.children.map((c) => c.id)
    const hasAllChildren = childIds.every((id) => form.value.menus.includes(id))

    if (hasAllChildren) {
        if (!form.value.menus.includes(menu.id)) {
            form.value.menus.push(menu.id)
        }
    } else {
        form.value.menus = form.value.menus.filter((id) => id !== menu.id)
    }
}

/* =========================
   flatpickr 설정
========================= */
const dayPickerConfig = {
    dateFormat: 'Y-m-d'
}

/* =========================
   권한 선택 (이탈 방지)
========================= */
const selectRole = async (role) => {
    if (selectedRole.value?.roleCd === role.roleCd) return

    if (isDirty.value) {
        const result = await Swal.fire({
            title: '수정 중인 내용이 있습니다',
            text: '저장하지 않고 이동하시겠습니까?',
            icon: 'warning',
            showCancelButton: true,
            confirmButtonText: '이동',
            cancelButtonText: '취소'
        })
        if (!result.isConfirmed) return
    }

    isCreateMode.value = false
    selectedRole.value = role
    form.value = JSON.parse(JSON.stringify(role))
    original.value = JSON.parse(JSON.stringify(role))
    isDirty.value = false
}

/* =========================
   신규 권한
========================= */
const openCreateUser = () => {
    isCreateMode.value = true
    selectedRole.value = {}
    form.value = {
        roleNm: '',
        roleCd: `NEW_${Date.now()}`,
        startDate: '',
        endDate: '',
        menus: []
    }

    original.value = {}
    isDirty.value = true
}

/* =========================
   Dirty 체크
========================= */
watch(
    form,
    () => {
        if (isCreateMode.value) return
        isDirty.value =
            JSON.stringify(form.value) !== JSON.stringify(original.value)
    },
    { deep: true }
)

const isModified = (key) => form.value[key] !== original.value[key]

/* =========================
   저장 / 취소 / 삭제 / 복제
========================= */
const saveRole = () => {
    if (isCreateMode.value) {
        roles.value.push({ ...form.value })
        isCreateMode.value = false
    } else {
        Object.assign(selectedRole.value, form.value)
    }
    original.value = JSON.parse(JSON.stringify(form.value))
    isDirty.value = false
}

const cancelEdit = () => {
    if (isCreateMode.value) {
        selectedRole.value = null
        form.value = {}
        isCreateMode.value = false
    } else {
        form.value = JSON.parse(JSON.stringify(original.value))
    }
    isDirty.value = false
}

const deleteRole = async () => {
    const result = await Swal.fire({
        title: '권한 삭제',
        text: `${form.value.roleNm} 권한을 삭제하시겠습니까?`,
        icon: 'warning',
        showCancelButton: true,
        confirmButtonText: '삭제',
        cancelButtonText: '취소'
    })
    if (!result.isConfirmed) return

    roles.value = roles.value.filter(
        (r) => r.roleCd !== selectedRole.value.roleCd
    )

    selectedRole.value = null
    form.value = {}
    original.value = {}
    isDirty.value = false
}

const duplicateRole = () => {
    const base = JSON.parse(JSON.stringify(form.value))
    const newRole = {
        ...base,
        roleNm: `${base.roleNm} (복제)`,
        roleCd: `COPY_${Date.now()}`
    }

    roles.value.push(newRole)
    selectedRole.value = newRole
    form.value = JSON.parse(JSON.stringify(newRole))
    original.value = JSON.parse(JSON.stringify(newRole))
    isDirty.value = false
}

/* =========================
   높이 계산
========================= */
const leftHeight = ref(400)
const rightScrollHeight = ref(0)
const HEADER_OFFSET = 185 // PageHeader + padding
const CARD_FOOTER_HEIGHT = 59 // footer 있을 때만

const calcHeights = () => {
    const viewport = window.innerHeight
    const baseHeight = viewport - HEADER_OFFSET

    // 좌측은 항상 동일
    leftHeight.value = baseHeight

    // 우측 Simplebar 높이
    let rightHeight = baseHeight
    // footer가 있을 때만 차감
    if (selectedRole.value) {
        rightHeight -= CARD_FOOTER_HEIGHT
    }

    rightScrollHeight.value = rightHeight
}
watch(selectedRole, () => {
    requestAnimationFrame(() => {
        calcHeights()
    })
})

onMounted(() => {
    calcHeights()
    window.addEventListener('resize', calcHeights)
})

onBeforeUnmount(() => {
    window.removeEventListener('resize', calcHeights)
})
</script>
