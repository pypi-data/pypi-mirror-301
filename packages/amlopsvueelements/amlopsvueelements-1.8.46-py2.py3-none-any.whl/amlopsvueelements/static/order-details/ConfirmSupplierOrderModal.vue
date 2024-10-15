<template>
  <div v-if="isOpen" class="supply-modal-mask">
    <div class="supply-modal-wrapper">
      <div class="supply-modal-container" ref="target">
        <div class="supply-modal-body">
          <OrderForm add-default-classes>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Confirm Supplier Order</div>
                <button @click.stop="emit('modal-close')"> <img width="12" height="12"
                    src="../../assets/icons/cross.svg" alt="delete" class="close"></button>
              </div>
            </template>
            <template #content>
              <div class="form-body-wrapper">
                <SelectField label-text="Supplier Reference" placeholder="Choose Reason" label="display"
                  v-model="selectedOption" :options="[]"></SelectField>
                <div class="w-full flex gap-3">
                  <InputField class="w-6/12" v-model="subject" :is-validation-dirty="v$?.form?.$dirty"
                    :errors="v$?.form?.jobs?.job_title?.$errors" label-text="Maximum Release Volume"
                    placeholder="Please enter quantity" />
                  <SelectField class="w-6/12" label-text="&nbsp;" placeholder="" label="description_plural"
                    v-model="selectedUom" :options="fuelQuantityUnits"></SelectField>
                </div>
                <div class="flex items-center justify-start pb-[0.75rem]">
                  <CheckboxField class="mb-0 mr-[0.25rem]" />
                  <p class="text-base whitespace-nowrap font-semibold text-main">Captain’s Request?</p>
                </div>
                <div class="w-full flex gap-x-3 mb-[0.75rem]">
                  <div class="w-6/12 min-w-[132px]">
                    <Label :required="false" label-text="Valid From (UTC)" class="whitespace-nowrap" />
                    <FlatPickr ref="departureDateRef" v-model="fromDateTime.date" :config="{
                      allowInput: true,
                      altInput: true,
                      altFormat: 'Y-m-d',
                      dateFormat: 'Y-m-d',
                    }" />
                  </div>
                  <div class="flex flex-col w-6/12">
                    <Label :required="false" label-text="&nbsp;" class="whitespace-nowrap" />
                    <FlatPickr v-model="fromDateTime.time" placeholder="Time" :config="{
                      altFormat: 'H:i',
                      altInput: true,
                      allowInput: true,
                      noCalendar: true,
                      enableTime: true,
                      time_24hr: true,
                      minuteIncrement: 1
                    }" class="!pr-0" />
                  </div>
                </div>
                <div class="w-full flex gap-x-3 mb-[0.75rem]">
                  <div class="w-6/12 min-w-[132px]">
                    <Label :required="false" label-text="Valid From (UTC)" class="whitespace-nowrap" />
                    <FlatPickr ref="departureDateRef" v-model="toDateTime.date" :config="{
                      allowInput: true,
                      altInput: true,
                      altFormat: 'Y-m-d',
                      dateFormat: 'Y-m-d',
                    }" />
                  </div>
                  <div class="flex flex-col w-6/12">
                    <Label :required="false" label-text="&nbsp;" class="whitespace-nowrap" />
                    <FlatPickr v-model="toDateTime.time" placeholder="Time" :config="{
                      altFormat: 'H:i',
                      altInput: true,
                      allowInput: true,
                      noCalendar: true,
                      enableTime: true,
                      time_24hr: true,
                      minuteIncrement: 1
                    }" class="!pr-0" />
                  </div>
                </div>
                <div class="flex items-center justify-start pb-[0.75rem] gap-3">
                  <button class="modal-button icon"><img height="20" width="20" :src="getImageUrl('assets/icons/paperclip.svg')"
                      alt="attachment"></button>
                  <p class="text-base whitespace-nowrap font-semibold text-main">Supplier Fuel Release</p>
                </div>
              </div>
            </template>
          </OrderForm>
        </div>
        <div class="supply-modal-footer">
          <button class="modal-button cancel" @click.stop="emit('modal-close')">Cancel</button>
          <button class="modal-button submit" :disabled="body.length > 200" @click.stop="onValidate()">Submit</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
import { onClickOutside } from '@vueuse/core'
import OrderForm from '@/components/forms/OrderForm.vue'
import { usePersonFormStore } from "@/stores/usePersonFormStore";
import { personRules } from "@/utils/rulesForForms";
import useVuelidate from "@vuelidate/core";
import InputField from "../forms/fields/InputField.vue";
import { storeToRefs } from "pinia";
import { useFetch } from "shared/composables";
import OrderReferences from "@/services/order/order-references";
import { notify } from "@/helpers/toast";
import Label from "../forms/Label.vue";
import TextareaField from "../forms/fields/TextareaField.vue";
import type { IPerson } from "@/types/order/order-reference.types";
import SelectField from "../forms/fields/SelectField.vue";
import ScrollBar from "../forms/ScrollBar.vue";
import CheckboxField from "../forms/fields/CheckboxField.vue";
import FlatPickr from "../FlatPickr/FlatPickr.vue";
import { getImageUrl } from "@/helpers";
import type { IFuelUom } from "@/types/order/order.types";

const props = defineProps({
  isOpen: Boolean,
  organisationId: {
    type: Number
  }
});

const emit = defineEmits(["modal-close", "modal-submit"]);

const selectedOption = ref('');
const selectedUom = ref();

const fromDateTime = ref({
  date: new Date(new Date().getTime() + (24 * 60 * 60 * 1000)).toLocaleDateString('en-CA'),
  time: '',
  timezone: 'Local'
})
const toDateTime = ref({
  date: new Date(new Date().getTime() + (48 * 60 * 60 * 1000)).toLocaleDateString('en-CA'),
  time: '',
  timezone: 'Local'
})

const target = ref(null);

const personFormStore = usePersonFormStore();

const { formModel } = storeToRefs(personFormStore);

const validationModel = ref({ form: formModel });

let v$ = ref(useVuelidate(personRules(), validationModel));

const subject = ref('');
const body = ref('');
const clientNote = ref('');
// onClickOutside(target, () => emit('modal-close'))

const onValidate = async () => {
  const isValid = await v$?.value?.$validate()
  if (!isValid) {
    return notify('Error while submitting, form is not valid!', 'error')
  } else {
    emit('modal-submit');
    emit('modal-close');
  }
}

const {
  loading: isLoadingFuelQuantityUnits,
  data: fuelQuantityUnits,
  callFetch: fetchFuelQuantityUnits
} = useFetch<IFuelUom[], () => Promise<IFuelUom[]>>(async () => {
  return await OrderReferences.fetchFuelQuantityUnits()
})

watch(() => props.organisationId, (value: any) => {
  fetchFuelQuantityUnits();
})


</script>

<style scoped lang="scss">
.supply-modal-mask {
  position: fixed;
  z-index: 1000;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
}

.supply-modal-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
}

.supply-modal-container {
  width: 520px;
  margin: auto;
  background-color: #fff;
  border-radius: .5rem;
  padding-top: 0.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

.form-body-wrapper {
  max-height: 500px;
}

.counter {
  color: rgba(133, 141, 173, 1);
  font-size: 12px;
  font-weight: 500;
}

.close {
  filter: brightness(0) saturate(100%) invert(80%) sepia(5%) saturate(2103%) hue-rotate(191deg) brightness(74%) contrast(83%);
}

.supply-modal-footer {
  padding: 0.5rem 1rem;
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  border-top-width: 1px;
  border-color: rgb(75 85 99 / 0.25);
}


.modal-button {
  display: flex;
  flex-shrink: 0;
  background-color: rgb(81 93 138) !important;
  padding: 0.5rem !important;
  padding-left: 1rem !important;
  padding-right: 1rem !important;
  color: rgb(255 255 255) !important;
  border-radius: 0.5rem !important;

  &.cancel {
    background-color: rgba(240, 242, 252, 1) !important;
    color: rgb(81 93 138) !important;
  }

  &.icon {
    background-color: rgba(240, 242, 252, 1) !important;
    color: rgb(81 93 138) !important;
    padding: 0.75rem !important;
    border-radius: 0.75rem !important;
  }

  &:disabled {
    background-color: rgb(241, 242, 246) !important;
    color: rgb(139, 148, 178) !important;
  }
}
</style>