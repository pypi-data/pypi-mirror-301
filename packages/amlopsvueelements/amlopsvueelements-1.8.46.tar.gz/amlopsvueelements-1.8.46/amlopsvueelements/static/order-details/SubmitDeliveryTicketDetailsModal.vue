<template>
  <div v-if="isOpen" class="supply-modal-mask">
    <div class="supply-modal-wrapper">
      <div class="supply-modal-container" ref="target">
        <div class="supply-modal-body">
          <OrderForm add-default-classes>
            <template #header>
              <div class="header w-full flex justify-between">
                <div class="text-[1.25rem] font-medium text-grey-1000">Submit Delivery Ticket Details</div>
                <button @click.stop="emit('modal-close')"> <img width="12" height="12"
                    src="../../assets/icons/cross.svg" alt="delete" class="close"></button>
              </div>
            </template>
            <template #content>
              <div class="form-body-wrapper flex flex-col items-center">
                <div class="w-full flex flex-col" v-for="(uplift, index) in formModel">
                  <Label :required="false" :label-text="`Uplift №${((index as number) + 1)}`"
                    class="whitespace-nowrap" />
                  <SelectField label-text="Aircraft" placeholder="Select Aircraft" label="display"
                    v-model="uplift.aircraft" :options="[]"></SelectField>
                  <div class="w-full flex gap-x-3 mb-[0.75rem]">
                    <div class="w-6/12 min-w-[132px]">
                      <Label :required="false" label-text="Date & Time of Uplift (UTC)" class="whitespace-nowrap" />
                      <FlatPickr v-if="fromDateTime.length === formModel.length" ref="departureDateRef"
                        v-model="fromDateTime[index as number].date" :config="{
                          allowInput: true,
                          altInput: true,
                          altFormat: 'Y-m-d',
                          dateFormat: 'Y-m-d',
                        }" />
                    </div>
                    <div class="flex flex-col w-6/12">
                      <Label :required="false" label-text="&nbsp;" class="whitespace-nowrap" />
                      <FlatPickr v-if="fromDateTime.length === formModel.length"
                        v-model="fromDateTime[index as number].time" placeholder="Time" :config="{
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
                  <div class="w-full flex gap-3">
                    <InputField class="w-6/12" v-model="uplift.fuel_quantity" :is-validation-dirty="v$?.form?.$dirty"
                      :errors="v$?.form?.jobs?.job_title?.$errors" label-text="Volume Uplifted"
                      placeholder="Please enter quantity" />
                    <SelectField class="w-6/12" label-text="&nbsp;" placeholder="" label="description_plural"
                      v-model="uplift.fuel_uom" :options="fuelQuantityUnits"></SelectField>
                  </div>
                  <SelectField label-text="Fuel Type" placeholder="Select Fuel Type" label="display"
                    v-model="uplift.fuel_type" :options="[]"></SelectField>
                  <SelectField label-text="IPA" placeholder="Select IPA" label="display" v-model="uplift.ipa"
                    :options="[]"></SelectField>
                  <SelectField label-text="Destination" placeholder="Select Destination" label="display"
                    v-model="uplift.destination" :options="[]"></SelectField>
                  <TextareaField class="w-full" v-model="uplift.comment" :is-validation-dirty="v$?.form?.$dirty"
                    :errors="v$?.form?.jobs?.job_title?.$errors" label-text="Comments"
                    placeholder="Please enter comments" />
                  <div class="flex items-center justify-start mb-[0.75rem] gap-3">
                    <button class="modal-button icon"><img height="20" width="20"
                        :src="getImageUrl('assets/icons/paperclip.svg')" alt="attachment"></button>
                    <p class="text-base whitespace-nowrap font-semibold text-main">Delivery Ticket</p>
                  </div>
                </div>
                <div class="w-full flex items-center pb-[0.75rem]">
                  <div class="divider-line"></div>
                  <div class="modal-button add gap-2 cursor-pointer" @click="upliftFormStore.addUplift">
                    <img src="../../assets/icons/plus.svg" alt="add">
                    Add Another Uplift
                  </div>
                  <div class="divider-line"></div>
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
import { personRules } from "@/utils/rulesForForms";
import useVuelidate from "@vuelidate/core";
import InputField from "../forms/fields/InputField.vue";
import { storeToRefs } from "pinia";
import { useFetch } from "shared/composables";
import OrderReferences from "@/services/order/order-references";
import { notify } from "@/helpers/toast";
import Label from "../forms/Label.vue";
import TextareaField from "../forms/fields/TextareaField.vue";
import SelectField from "../forms/fields/SelectField.vue";
import CheckboxField from "../forms/fields/CheckboxField.vue";
import FlatPickr from "../FlatPickr/FlatPickr.vue";
import { getImageUrl } from "@/helpers";
import type { IFuelUom } from "@/types/order/order.types";
import { useUpliftFormStore } from "@/stores/useUpliftFormStore";

const props = defineProps({
  isOpen: Boolean,
  organisationId: {
    type: Number
  }
});

const emit = defineEmits(["modal-close", "modal-submit"]);

const fromDateTime = ref([{
  date: new Date(new Date().getTime() + (24 * 60 * 60 * 1000)).toLocaleDateString('en-CA'),
  time: '',
}])

const tempDate = ref('');

const target = ref(null);

const upliftFormStore = useUpliftFormStore();

const { formModel } = storeToRefs(upliftFormStore);

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


watch(() => formModel.value, (value: any) => {
  console.log(value);
  if (value.length > fromDateTime.value.length) {
    fromDateTime.value.push({
      date: new Date(new Date().getTime() + (24 * 60 * 60 * 1000)).toLocaleDateString('en-CA'),
      time: '',
    })
  }
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

  &.add {
    background-color: transparent !important;
    color: rgba(81, 93, 138, 1) !important;
    width: fit-content !important;

    img {
      filter: brightness(0) saturate(100%) invert(37%) sepia(12%) saturate(1572%) hue-rotate(190deg) brightness(94%) contrast(89%);
    }
  }
}

.divider-line {
  width: 100%;
  min-width: 50px;
  height: 1px;
  border-top: 1px solid rgba(223, 226, 236, 1);
}
</style>