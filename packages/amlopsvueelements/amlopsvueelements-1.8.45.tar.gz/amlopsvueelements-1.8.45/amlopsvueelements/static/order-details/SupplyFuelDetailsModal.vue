<template>
  <div v-if="isOpen" class="supply-modal-mask">
    <div class="supply-modal-wrapper">
      <div class="supply-modal-container" ref="target">
        <div class="supply-modal-header flex justify-between">Supplier Fuel Pricing Details
          <img width="12" height="12" src="../../assets/icons/cross.svg" alt="delete" class="close cursor-pointer"
            @click="emit('modal-close')">
        </div>
        <div class="py-[1.5rem] px-[0.75rem] min-h-[70vh] flex items-center" v-if="isLoadingSupplierFuelDetails">
          <Loading></Loading>
        </div>
        <ScrollBar v-else class="my-0">
          <div class="supply-modal-body">
            <div class="supply-modal-body-header flex gap-4">
              <div class="supply-modal-body-header-col w-6/12 flex flex-col gap-2">
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Location</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.airport?.full_repr ?? '--'
                    }}
                  </div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Into-Plane Agent</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.ipa?.full_repr ??
                    '--' }}
                  </div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Pricing Type</div>
                  <div class="supply-modal-body-header-el-data w-6/12">
                    <div v-if="!supplyFuelDetails?.fuel_price?.pricing_link">{{ '--' }}</div>
                    <div v-else v-html="supplyFuelDetails?.fuel_price?.pricing_link"></div>
                  </div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Handler-Specific Pricing</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.handler_specific_pricing ?
                    supplyFuelDetails?.handler_specific_pricing?.name :
                    'No' }}</div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Apron-Specific Pricing</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.apron_specific_pricing ?
                    supplyFuelDetails?.apron_specific_pricing?.name :
                    'No' }}</div>
                </div>
              </div>
              <div class="supply-modal-body-header-col w-6/12 flex flex-col gap-2">
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Supplier</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.supplier?.full_repr
                    ?? '--' }}</div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Intermediate Supplier</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.intermediate_supplier ?
                    supplyFuelDetails?.intermediate_supplier?.full_repr :
                    'No' }}</div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Delivery Method</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.delivery_method ?
                    supplyFuelDetails?.delivery_method.name :
                    'TBC' }}</div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Client-Specific Pricing</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.client_specific_pricing ?
                    supplyFuelDetails?.client_specific_pricing?.name
                    :
                    'No' }}</div>
                </div>
                <div class="supply-modal-body-header-el flex gap-2">
                  <div class="supply-modal-body-header-el-name w-6/12">Terminal-Specific Pricing</div>
                  <div class="supply-modal-body-header-el-data w-6/12">{{ supplyFuelDetails?.terminal_specific_pricing ?
                    supplyFuelDetails?.terminal_specific_pricing?.name :
                    'No' }}</div>
                </div>
              </div>
            </div>
            <div class="supply-modal-body-content-wrap flex">
              <div class="supply-modal-body-content w-full flex flex-col gap-2">
                <div class="supply-modal-body-content-block" v-if="supplyFuelDetails?.issues.length > 0">
                  <div class="supply-modal-body-content-block-header issues p-[0.75rem]">
                    <img width="20" height="20" src="../../assets/icons/alert.svg" alt="warn" class="warn">
                    {{ props.isOpenRelease ? supplyFuelDetails?.issues.length + 1 : supplyFuelDetails?.issues.length }}
                    {{ (props.isOpenRelease && supplyFuelDetails?.issues.length >= 1) ||
                      supplyFuelDetails?.issues.length >= 2 ? 'Issues' : 'Issue' }} Detected
                  </div>
                  <div
                    class="supply-modal-body-content-block-body px-[0.75rem] py-[1rem] pl-[1.5rem] gap-3 flex flex-col">
                    <div class="issue-html" v-if="props.isOpenRelease">
                      This is an open fuel release, and as such an indicative fuel quantity is used. Additionally, as
                      the destination is not known, the flight destination for the order is treated as domestic to
                      represent the worst-case exposure scenario.
                    </div>
                    <div class="issue-html" v-for="issue in supplyFuelDetails?.issues" v-html="issue">
                    </div>
                  </div>
                </div>
                <div class="supply-modal-body-content-block">
                  <div class="supply-modal-body-content-block-header p-[0.75rem]">
                    Fuel Pricing
                  </div>
                  <div class="supply-modal-body-content-block-body flex px-[0.75rem] py-[1rem]">
                    <div class="supply-modal-body-content-block-body-name w-4/12">{{
                      supplyFuelDetails?.fuel_price?.fuel?.name
                    }}
                    </div>
                    <div class="supply-modal-body-content-block-body-desc w-6/12 relative flex items-center gap-2">
                      {{ supplyFuelDetails?.fuel_price?.unit_price }} {{
                        supplyFuelDetails?.fuel_price?.original_pricing_unit?.description }} X {{
                        addThousandSeparators(supplyFuelDetails?.fuel_price?.converted_uplift_qty) }} {{
                        supplyFuelDetails?.fuel_price?.uom?.description_plural }}
                      <div class="supply-modal-body-content-block-body-note hover-wrap contents flex items-center">
                        <img width="12" height="12" src="../../assets/icons/info-circle.svg" alt="warn" class="warn">
                        <div class="supply-modal-body-tooltip left-tooltip">
                          <div v-for="note in supplyFuelDetails?.fuel_price?.notes" v-html="'● ' + note"></div>
                        </div>
                      </div>
                    </div>
                    <div class="supply-modal-body-content-block-body-value w-2/12">{{
                      formatNumber(supplyFuelDetails?.fuel_price?.amount) }}
                      {{ supplyFuelDetails?.currency?.code }} </div>
                  </div>
                </div>
                <div class="supply-modal-body-content-block">
                  <div class="supply-modal-body-content-block-header p-[0.75rem]">
                    Fees
                  </div>
                  <div
                    class="results supply-modal-body-content-block-body flex px-[0.75rem] py-6 flex justify-center border border-transparent rounded"
                    v-if="supplyFuelDetails && (Object.keys(supplyFuelDetails?.fees?.list).length === 0 || !supplyFuelDetails.hasOwnProperty('fees'))">
                    <div class="supply-modal-body-content-block-body-name flex flex-col items-center">No fees calculated
                      for
                      this scenario</div>
                  </div>
                  <div class="supply-modal-body-content-block-body flex px-[0.75rem] py-[1rem]" v-else
                    v-for="(fee, key) in supplyFuelDetails?.fees?.list" :key="key">
                    <div class="supply-modal-body-content-block-body-name w-4/12">
                      {{ fee.display_name ?? 'Custom Fee' }}
                      <div class="supply-modal-body-content-block-body-note hover-wrap contents flex items-center">
                        <img width="12" height="12" src="../../assets/icons/info-circle.svg" alt="warn" class="warn">
                        <div class="supply-modal-body-tooltip">
                          <div v-for="note in fee.notes" v-html="'● ' + note"></div>
                        </div>
                      </div>
                    </div>
                    <div class="supply-modal-body-content-block-body-desc w-6/12">
                    </div>
                    <div class="supply-modal-body-content-block-body-value w-2/12">{{ formatNumber(fee?.amount) }} {{
                      supplyFuelDetails?.currency?.code }}</div>
                  </div>
                </div>
                <div class="supply-modal-body-content-block">
                  <div class="supply-modal-body-content-block-header p-[0.75rem]">
                    Taxes
                  </div>
                  <div
                    class="results supply-modal-body-content-block-body flex px-[0.75rem] py-6 flex justify-center border border-transparent rounded"
                    v-if="supplyFuelDetails && (Object.keys(supplyFuelDetails?.taxes?.list).length === 0 || !supplyFuelDetails.hasOwnProperty('taxes'))">
                    <div class="supply-modal-body-content-block-body-name flex flex-col items-center">No taxes
                      calculated for
                      this scenario</div>
                  </div>
                  <div class="supply-modal-body-content-block-body flex flex-col" v-else>
                    <div class="flex w-full">
                      <div class="supply-modal-body-content-block-body-header w-6/12 text-center">
                        <div class="el-border supply-modal-body-content-block-body-header-el my-[0.5rem]">
                          Official Taxes
                        </div>
                      </div>
                      <div class="supply-modal-body-content-block-body-header w-6/12 text-center">
                        <div class="supply-modal-body-content-block-body-header-el my-[0.5rem]">Supplier-Defined Taxes
                        </div>
                      </div>
                    </div>
                    <div class="flex w-full" v-for="(tax, key, index) in supplyFuelDetails?.taxes?.list" :key="key">
                      <div class="el-border w-6/12 issues flex px-[0.75rem] py-[1rem] items-center relative">
                        <div class="supply-modal-body-content-block-body-name w-8/12">{{ key }} <div
                            class="supply-modal-body-content-block-body-note hover-wrap contents flex items-center">
                            <img width="12" height="12" src="../../assets/icons/info-circle.svg" alt="warn"
                              class="warn">
                            <div class="supply-modal-body-tooltip">
                              <div v-for="note in supplyFuel.results[resultIndex].tax_notes" v-html="note"></div>
                            </div>
                          </div>
                        </div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(tax?.official?.amount)
                          }}
                          {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                      <div class="w-6/12 issues flex px-[0.75rem] py-[1rem] items-center relative">
                        <div class="supply-modal-body-content-block-body-name w-8/12">{{ key }} <div
                            class="supply-modal-body-content-block-body-note hover-wrap contents flex items-center">
                            <img width="12" height="12" src="../../assets/icons/info-circle.svg" alt="warn"
                              class="warn">
                            <div class="supply-modal-body-tooltip left-tooltip">
                              <div v-for="note in supplyFuel.results[resultIndex].tax_notes" v-html="note"></div>
                            </div>
                          </div>
                        </div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(tax?.supplier?.amount)
                          }}
                          {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="supply-modal-body-content-block">
                  <div class="supply-modal-body-content-block-header p-[0.75rem]">
                    Total cost
                  </div>
                  <div class="supply-modal-body-content-block-body flex flex-col">
                    <div class="flex w-full">
                      <div class="supply-modal-body-content-block-body-header w-6/12 pl-3">
                        <div class="el-border supply-modal-body-content-block-body-header-el my-[0.5rem]">
                          With Official Taxes
                        </div>
                      </div>
                      <div class="supply-modal-body-content-block-body-header w-6/12 pl-3 ">
                        <div class="supply-modal-body-content-block-body-header-el my-[0.5rem]">With Supplier-Defined
                          Taxes</div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Fuel</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.fuel_price?.amount) }} {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                      <div class="w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Fuel</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.fuel_price?.amount) }} {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Fees</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.fees?.total) }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                      <div class="w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Fees</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.fees?.client_total) }} {{ supplyFuelDetails?.currency?.code }}
                        </div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Taxes</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.taxes?.official_total) }} {{ supplyFuelDetails?.currency?.code
                          }}</div>
                      </div>
                      <div class="w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Taxes</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.taxes?.supplier_total) }} {{ supplyFuelDetails?.currency?.code
                          }}</div>
                      </div>
                    </div>
                    <div class="flex w-full">
                      <div class="el-border results w-6/12 flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Total Uplift Cost</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.total_official_taxes) }} {{ supplyFuelDetails?.currency?.code
                          }}</div>
                      </div>
                      <div class="w-6/12 results flex px-[0.75rem] py-[1rem] items-center">
                        <div class="supply-modal-body-content-block-body-name w-8/12">Total Uplift Cost</div>
                        <div class="supply-modal-body-content-block-body-value w-4/12">{{
                          formatNumber(supplyFuelDetails?.total) }} {{ supplyFuelDetails?.currency?.code }}</div>
                      </div>
                    </div>
                  </div>
                </div>
                <div class="supply-modal-body-content-block">
                  <div class="supply-modal-body-content-block-header p-[0.75rem]">
                    Exchange Rates
                  </div>
                  <div class="supply-modal-body-content-block-body flex px-[0.75rem] py-[1rem]">
                    <div class="supply-modal-body-content-block-body-name w-8/12 flex flex-col">Open Exchange Rates
                      <div class="supply-modal-body-content-block-body-sub">Valid at {{
                        toRateTime(supplyFuel?.scenario?.used_currency_rates?.[Object.keys(supplyFuel?.scenario?.used_currency_rates)[0]]?.timestamp
                          + '000') }}</div>
                    </div>
                    <div class="supply-modal-body-content-block-body-value w-4/12 flex items-center justify-end">
                      {{
                        supplyFuel?.scenario?.used_currency_rates?.[Object.keys(supplyFuel?.scenario?.used_currency_rates)[0]]?.rate
                      }}
                      {{ JSON.parse(Object.keys(supplyFuel?.scenario?.used_currency_rates)[0])[0] }}
                      -> {{ JSON.parse(Object.keys(supplyFuel?.scenario?.used_currency_rates)[0])[1] }}</div>
                  </div>
                </div>
                <div class="supply-modal-body-content-block">
                  <div class="supply-modal-body-content-block-header p-[0.75rem]">
                    Fuel-related NOTAMs
                  </div>
                  <div class="supply-modal-body-content-block-body flex flex-col px-[0.75rem] py-[0.75rem]"
                    v-if="supplyFuelDetails?.notams?.length > 0">
                    <div class="supply-modal-body-content-block-body-name flex flex-col"
                      v-for="notam in supplyFuelDetails?.notams">
                      <div>{{ notam.effective_start }} - {{ notam.effective_end ?? 'PERM' }} Status: {{ notam.status }}
                      </div>
                      <div v-text="notam.text"></div>
                    </div>
                    <div class="supply-modal-body-content-block-body-sub">The FAA NOTAMs API was last chacked for this
                      location
                      at {{ supplyFuelDetails?.notams_last_check }}</div>
                  </div>
                  <div
                    class="results supply-modal-body-content-block-body flex flex-col items-center justify-center px-[0.75rem] py-6"
                    v-else>
                    <div class="supply-modal-body-content-block-body-name flex flex-col items-center">No fuel-related
                      NOTAMs
                      found</div>
                    <div class="supply-modal-body-content-block-body-sub">The FAA NOTAMs API was last chacked for this
                      location
                      at {{ supplyFuelDetails?.notams_last_check }}</div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </ScrollBar>
        <div class="supply-modal-footer flex justify-end">
          <div class="supply-modal-footer-el flex justify-between w-6/12">
            <div class="supply-modal-footer-el-name" v-if="!isLoadingSupplierFuelDetails">
              Total Uplift Cost
            </div>
            <div class="supply-modal-footer-el-value" v-if="!isLoadingSupplierFuelDetails">
              {{ formatNumber(supplyFuelDetails?.total) }} {{
                supplyFuelDetails?.currency?.code }}
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, watch } from "vue";
import { onClickOutside } from '@vueuse/core'
import ScrollBar from "../forms/ScrollBar.vue";
import { addThousandSeparators, formatNumber, toRateTime } from "@/helpers/order";
import { useFetch } from "shared/composables";
import OrderReferences from "@/services/order/order-references";
import Loading from "../forms/Loading.vue";

const props = defineProps({
  isOpen: Boolean,
  isOpenRelease: Boolean,
  supplyFuel: {
    type: Object,
    default: null
  },
  resultIndex: {
    type: Number,
    default: 0
  }
});

const emit = defineEmits(["modal-close", "modal-submit"]);

const target = ref(null);

const isLoadingSupplierFuelDetails = ref(true);

onClickOutside(target, () => emit('modal-close'))

const {
  data: supplyFuelDetails,
  callFetch: fetchSupplierFuelDetails,
} = useFetch<any, (supplierId: number, detailsId: number) => Promise<any>>(async (supplierId: number, detailsId: number) => {
  const data = await OrderReferences.fetchSupplierFuelDetails(supplierId, detailsId)
  isLoadingSupplierFuelDetails.value = false;
  return data;
})


watch([() => props.resultIndex, () => props.supplyFuel], ([a, b]) => {
  if (a !== null && b !== null) {
    isLoadingSupplierFuelDetails.value = true;
    fetchSupplierFuelDetails(b?.id, b?.results[a].key)
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
  width: 700px;
  margin: auto;
  background-color: #fff;
  border-radius: .5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.33);
}

.form-body-wrapper {
  max-height: 820px;
  overflow-y: auto;
}

.close {
  filter: brightness(0) saturate(100%) invert(80%) sepia(5%) saturate(2103%) hue-rotate(191deg) brightness(74%) contrast(83%);
}

.supply-modal-header {
  color: rgba(39, 44, 63, 1);
  font-size: 18px;
  font-weight: 600;
  padding: 1.25rem 1.5rem 1.25rem 1.5rem;
}

.supply-modal-body {
  max-height: 70vh;

  &-header {
    border-top: 1px solid rgba(223, 226, 236, 1);
    border-bottom: 1px solid rgba(223, 226, 236, 1);
    padding: 1rem 1.5rem 1rem 1.5rem;

    &-el {
      align-items: baseline;

      &-name {
        font-size: 13px;
        color: rgba(82, 90, 122, 1);
        font-weight: 500;
      }

      &-data {
        font-size: 14px;
        color: rgba(21, 28, 53, 1);
        font-weight: 500;
      }
    }

    &-content {
      padding: 0.75rem;
    }
  }

  .issues {
    background-color: rgba(255, 161, 0, 0.08);
  }

  .results {
    background-color: rgb(246, 248, 252);
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);
  }

  &-tooltip {
    display: none;
    position: absolute;
    background-color: rgb(81, 93, 138);
    color: rgb(255, 255, 255);
    font-size: 12px;
    font-weight: 400;
    z-index: 10;
    padding: 0.5rem;
    border-radius: 0.5rem;
    bottom: 1.5rem;
    left: 0;
    min-width: 27vw;

    &::before {
      content: "";
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: rgb(81, 93, 138);
      transform: rotate(45deg);
      left: 6.7rem;
      bottom: -5px;
    }

    &.left-tooltip {
      right: 0;
      left: unset;

      &::before {
        right: 50%;
        left: unset;
        bottom: -5px;
      }
    }
  }


  &-content {
    background-color: rgba(239, 241, 246, 1);

    &-wrap {
      background-color: rgba(239, 241, 246, 1);
    }

    &-block {
      border: 1px solid rgba(223, 226, 236, 1);
      border-radius: 6px;
      background-color: rgb(255, 255, 255);

      &-header {
        color: rgba(21, 28, 53, 1);
        font-size: 15px;
        font-weight: 600;
        border-bottom: 1px solid rgba(223, 226, 236, 1);
      }

      &-body {
        color: rgba(39, 44, 63, 1);
        font-size: 14px;
        font-weight: 500;

        &-header {
          background-color: rgba(246, 248, 252, 1);
          color: rgba(82, 90, 122, 1);
          font-size: 11px;
          font-weight: 500;
        }

        &-name {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 500;
          position: relative;
        }

        &-sub {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }

        &-desc {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 400;
        }

        &-value {
          color: rgba(39, 44, 63, 1);
          font-size: 13px;
          font-weight: 600;
          text-align: end;
        }

        .issue-html {
          position: relative;

          &::before {
            content: '';
            position: absolute;
            height: 19px;
            width: 4px;
            background-color: rgba(254, 161, 22, 1);
            border-radius: 2px;
            left: -0.8rem;
          }
        }
      }
    }
  }

  .hover-wrap {
    &:hover {
      .supply-modal-body-tooltip {
        display: block;
      }
    }
  }
}

.supply-modal-footer {
  display: flex;
  justify-content: flex-end;
  gap: 0.5rem;
  border-top-width: 1px;
  border-color: rgb(75 85 99 / 0.25);
  background-color: rgba(246, 248, 252, 1);
  border-radius: 0 0 0.5rem 0.5rem;
  padding: 1.25rem 1.5rem 1.25rem 1.5rem;

  &-el {
    &-name {
      color: rgba(39, 44, 63, 1);
      font-size: 13px;
      font-weight: 500;
    }

    &-value {
      color: rgba(39, 44, 63, 1);
      font-size: 13px;
      font-weight: 600;
    }
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
  }
}
</style>