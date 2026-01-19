<template>
    <b-modal
        :model-value="modelValue"
        :title="modalTitle"
        centered
        scrollable
        @hidden="reset"
        @update:modelValue="emit('update:modelValue', $event)"
    >
        <b-form>
            <b-row class="g-2 row-cols-1">
                <!-- 권한명 -->
                <b-col class="hstack gap-2">
                    <label class="col-form-label col-3 required">
                        권한명
                    </label>
                    <b-form-input
                        v-model="form.roleNm"
                        placeholder="권한명을 입력하세요"
                    />
                </b-col>

                <!-- 권한 코드 -->
                <b-col class="hstack gap-2">
                    <label class="col-form-label col-3 required">
                        권한 코드
                    </label>
                    <b-form-input
                        v-model="form.roleCd"
                        placeholder="예: RD0004"
                    />
                </b-col>

                <!-- 유효기간 (day picker 2개) -->
                <b-col class="hstack gap-2 align-items-center">
                    <label class="col-form-label col-3"> 유효기간 </label>

                    <flat-pickr
                        v-model="startDate"
                        :config="dayPickerConfig"
                        class="form-control"
                        placeholder="시작일"
                    />

                    <span>~</span>

                    <flat-pickr
                        v-model="endDate"
                        :config="dayPickerConfig"
                        class="form-control"
                        placeholder="종료일"
                    />
                </b-col>
            </b-row>
        </b-form>

        <!-- footer -->
        <template #footer>
            <b-button variant="light" @click="close"> 취소 </b-button>
            <b-button variant="primary" @click="save"> 저장 </b-button>
        </template>
    </b-modal>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import FlatPickr from 'vue-flatpickr-component'
import 'flatpickr/dist/flatpickr.css'
import dayjs from 'dayjs'
import { Korean } from 'flatpickr/dist/l10n/ko.js'

/* =========================
   Props / Emits
========================= */
const props = defineProps({
    modelValue: Boolean,
    editData: Object // ← edit 모드 대응
})

const emit = defineEmits(['update:modelValue', 'saved'])

/* =========================
   Form
========================= */
const defaultForm = () => ({
    roleNm: '',
    roleCd: '',
    period: '' // YYYY-MM-DD ~ YYYY-MM-DD
})

const form = ref(defaultForm())

/* =========================
   날짜 상태
========================= */
const startDate = ref(null)
const endDate = ref(null)

/* flatpickr day picker 설정 */
const dayPickerConfig = {
    dateFormat: 'Y-m-d',
    locale: Korean
}

/* 날짜 변경 시 period 자동 생성 */
watch([startDate, endDate], ([start, end]) => {
    if (start && end) {
        const s = dayjs(start).format('YYYY-MM-DD')
        const e = dayjs(end).format('YYYY-MM-DD')
        form.value.period = `${s} ~ ${e}`
    } else {
        form.value.period = ''
    }
})

/* =========================
   Edit 데이터 반영
========================= */
watch(
    () => props.editData,
    (val) => {
        if (!val) return

        form.value = {
            roleNm: val.roleNm,
            roleCd: val.roleCd,
            period: val.period || ''
        }

        if (val.period) {
            const [s, e] = val.period.split(' ~ ')
            startDate.value = s
            endDate.value = e
        }
    },
    { immediate: true }
)

/* =========================
   Modal Title
========================= */
const modalTitle = computed(() => (props.editData ? '권한 수정' : '권한 추가'))

/* =========================
   Actions
========================= */
const save = () => {
    if (!form.value.roleNm || !form.value.roleCd) return

    emit('saved', {
        ...form.value
    })

    close()
}

const close = () => {
    emit('update:modelValue', false)
}

const reset = () => {
    form.value = defaultForm()
    startDate.value = null
    endDate.value = null
}
</script>
