<template>
  <div class="w-full h-full flex flex-col gap-2">
    <div class="compliance-step bg-white w-full border border-transparent rounded-md">
      <div class="compliance-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="compliance-step-header-name">Management Approval</div>
      </div>
      <div class="compliance-step-content compliance-status w-full flex p-[0.75rem] gap-2">
        <div class="compliance-step-content-el-name flex items-center">Status</div>
        <div class="compliance-step-content-el-value py-[0.25rem] px-[0.75rem]">Confirmed</div>
      </div>
    </div>
    <div class="compliance-step bg-white w-full border border-transparent rounded-md">
      <div class="compliance-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="compliance-step-header-name">Compliance Checks</div>
      </div>
      <div class="compliance-step-content w-full flex flex-col">
        <div class="compliance-step-content-header-wrap w-full flex items-center">
          <div class="compliance-step-content-col pl-[0.75rem] py-[0.5rem] w-6/12">
            <div class="compliance-step-content-col-header uppercase el-border">Sanctions</div>
          </div>
          <div class="compliance-step-content-col w-6/12">
            <div class="compliance-step-content-col-header px-[0.75rem] py-[0.5rem] uppercase">Supplier Restrictions
            </div>
          </div>
        </div>
        <div class="compliance-step-content-data-wrap w-full flex items-start">
          <div class="compliance-step-content-col flex flex-col w-6/12">
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Client</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Operator</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-yellow">
                  <div class="icon"></div>
                </div>Needs Reviewing
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Aircraft</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Uplift Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Destination Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
          </div>
          <div class="compliance-step-content-col flex flex-col w-6/12 el-border-left">
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Aircraft</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-red">
                  <div class="icon"></div>
                </div>Sanctioned
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Aircraft Registration Prefix</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-gray">
                  <div class="icon"></div>
                </div>Not Applicable
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Uplift Airport</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Destination Airport</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Uplift Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
            <div class="compliance-step-content-col-data flex px-[0.75rem] py-[0.5rem]">
              <div class="compliance-step-content-col-data-name w-5/12">Destination Country</div>
              <div class="compliance-step-content-col-data-value w-7/12 flex gap-1">
                <div class="circle circle-green">
                  <div class="icon"></div>
                </div>OK
              </div>
            </div>
          </div>
        </div>
      </div>
      <div class="compliance-step-content-divider py-[0.5rem] px-[0.75rem] uppercase">Aircraft Recent Destinations</div>
      <div class="compliance-step-content w-full flex flex-col">
        <div class="compliance-step-content-destination-el flex w-full py-5 px-[0.75rem]"
          v-for="el in mockDestinations">
          <div class="compliance-step-content-destination-el-name w-4/12">{{ el.date }}</div>
          <div class="compliance-step-content-destination-el-name w-4/12">{{ el.airport }}</div>
          <div class="compliance-step-content-destination-el-name w-4/12">{{ el.country }}</div>
        </div>
      </div>
      <div class="compliance-step-content-divider py-[0.5rem] px-[0.75rem] uppercase">Fuel-Related NOTAMs</div>
      <div class="compliance-step-content w-full flex flex-col">
        <div class="compliance-step-content-activity border-0 rounded-lg pl-[0.75rem] flex"
          v-for="activity in mockActivity" :key="activity.date">
          <div class="compliance-step-info-side flex flex-col items-center">
            <div class="line-top"></div>
            <div class="circle"></div>
            <div class="line-bottom"></div>
          </div>
          <div class="compliance-step-info-wrap p-[0.75rem] flex flex-col">
            <div class="compliance-step-info flex justify-between">
              <div class="compliance-step-info-date">{{ activity.date }}</div>
            </div>
            <div class="compliance-step-data">{{ activity.description }}</div>
          </div>
        </div>
      </div>
      <div class="compliance-step-content w-full flex py-8 px-[0.75rem] flex flex-col" v-if="isLoadingCompliance">
        <Loading />
      </div>
    </div>
    <div class="compliance-step bg-white w-full border border-transparent rounded-md">
      <div class="compliance-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="compliance-step-header-name">Client Credit Exposure</div>
      </div>
      <div class="compliance-step-content compliance-credit w-full flex flex-col p-[0.75rem] gap-2">
        <CreditExposure :confirmed="mockCredit.confirmed" :limit="mockCredit.limit" :maximum="mockCredit.maximum"
          :open="mockCredit.open" :is-open-release="order?.fuel_order?.is_open_release" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch, type PropType, type Ref } from 'vue';
import { useFetch } from 'shared/composables';
import OrderReferences from '@/services/order/order-references';
import type { IOrder } from '@/types/order/order.types';
import Loading from '../forms/Loading.vue';
import CreditExposure from '../datacomponent/CreditExposure.vue';

const props = defineProps({
  isLoading: {
    type: Boolean as PropType<boolean>,
    default: false
  },
  order: {
    type: Object as PropType<IOrder>,
    default: null
  }
})

const mockDestinations = ref([{
  date: '2024-07-24',
  airport: 'Newcastle Airport (EGNT/NCL)',
  country: 'United Kingdom'
}, {
  date: '2024-07-24',
  airport: 'Newcastle Airport (EGNT/NCL)',
  country: 'United Kingdom'
}])
const mockCredit = ref({
  confirmed: 20000,
  open: 30000,
  maximum: 60000,
  limit: 100000,
})
const mockActivity = [{ date: new Date().toDateString(), description: 'Admin Edit Session: End. A really long message there to show the correct expansion of the element on the side. This element should be way bigger then the other.' },
{ date: new Date().toDateString(), description: 'Admin Edit Session: End' }
]

const isLoadingCompliance = ref(false);

const {
  data: compliance,
  callFetch: fetchCompliance,
} = useFetch<any, (order: any) => Promise<any>>(async (order: any) => {
  // const data = await OrderReferences.fetchSupplierFuelDetails(supplierId, detailsId)
  // console.log(data);
  isLoadingCompliance.value = false;
  return []
  // return data;
})

watch(() => props.order, (order: IOrder) => {
  fetchCompliance(order);
})

</script>

<style lang="scss">
.compliance-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-4 rounded-xl #{!important};
  }

  .el-border {
    border-right: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid rgba(239, 241, 246, 1)
    }
  }

  .el-border-left {
    border-left: 1px solid rgb(223, 226, 236);

    &-light {
      border-right: 1px solid rgba(239, 241, 246, 1)
    }
  }

  .circle {
    width: 20px;
    height: 20px;
    display: flex;
    justify-content: center;
    align-items: center;
    border-radius: 50%;

    .icon {
      height: 12px;
      width: 12px;
      z-index: 1;
    }

    &-green {
      background-color: rgba(11, 161, 125, 0.12);

      .icon {
        background-image: url("../../assets/icons/status-check.svg");
      }
    }

    &-yellow {
      background-color: rgba(254, 161, 22, 0.12);

      .icon {
        background-image: url("../../assets/icons/status-alert.svg");
      }
    }

    &-red {
      background-color: rgba(254, 98, 98, 1);

      .icon {
        background-image: url("../../assets/icons/status-close.svg");
      }
    }

    &-gray {
      background-color: rgba(139, 148, 178, 0.12);

      .icon {
        background-image: url("../../assets/icons/status-help.svg");
      }
    }
  }


  &-header {
    color: rgba(21, 28, 53, 1);
    font-size: 18px;
    font-weight: 600;
  }

  &-content {

    &.compliance-status {
      border-top: 1px solid rgba(239, 241, 246, 1);
    }

    &-el {
      &-name {
        color: rgba(82, 90, 122, 1);
        font-size: 13px;
        font-weight: 500;
        min-width: 100px;
      }

      &-value {
        background-color: rgba(254, 161, 22, 1);
        color: rgb(255, 255, 255);
        border-radius: 6px;
        border: 1px solid transparent;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;
      }
    }

    &-data-wrap {
      border-bottom: 1px solid rgba(239, 241, 246, 1);
      background-color: rgba(255, 255, 255, 1);
    }

    &-header-wrap {
      background-color: rgb(246, 248, 252);
    }

    &-header-big-wrap {
      background-color: rgba(246, 248, 252, 1);
    }

    &-divider {
      text-transform: capitalize;
      background-color: rgba(246, 248, 252, 1);
      color: rgba(82, 90, 122, 1);
      font-size: 12px;
      font-weight: 500;
    }


    &-col {
      &-header {
        color: rgba(82, 90, 122, 1);
        font-size: 11px;
        font-weight: 500;
        background-color: rgb(246, 248, 252);
      }

      &-data {
        color: rgba(133, 141, 173, 1);
        font-size: 13px;
        font-weight: 400;
        background-color: rgba(256, 256, 256, 1);

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 13px;
          font-weight: 500;
        }

        &-value {
          color: rgba(21, 28, 53, 1);
          font-size: 14px;
          font-weight: 500;
        }
      }
    }

    &-destination-el {
      &-name {
        color: rgba(39, 44, 63, 1);
        font-size: 13px;
        font-weight: 500;
      }

      border-bottom: 1px solid rgba(239, 241, 246, 1);
    }

    &-activity {

      &:nth-of-type(2) {
        background-color: rgba(246, 248, 252, 1);
        ;
      }

      &:first-of-type {
        .compliance-step-info-side {
          padding-top: 12px;
        }

        .line-top {
          display: none;
        }
      }

      &:last-of-type {
        .line-bottom {
          display: none;
        }
      }

      .compliance-step-info {
        position: relative;

        &-date {
          color: rgba(39, 44, 63, 1);
          font-weight: 600;
          font-size: 14px;
        }

        &-side {
          .circle {
            height: 8px;
            width: 8px;
            background-color: rgba(255, 255, 255, 1);
            border: 2px solid rgba(125, 148, 231, 1);
            border-radius: 50%;
            left: -1rem;
          }

          .line-bottom {
            width: 1px;
            background-color: rgba(223, 226, 236, 1);
            border: 1px solid rgba(223, 226, 236, 1);
            height: 100%;
            top: 6px;
            left: 1.5px;
          }


          .line-top {
            width: 1px;
            background-color: rgba(223, 226, 236, 1);
            border: 1px solid rgba(223, 226, 236, 1);
            height: 12px;
            top: 6px;
            left: 1.5px;
          }
        }
      }


      .compliance-step-data {
        color: rgba(39, 44, 63, 1);
        font-weight: 400;
        font-size: 15px;
      }
    }
  }

  .roi {
    border-top: 1px solid rgba(239, 241, 246, 1);

    &-inputs-wrap:first-of-type {
      border-right: 1px solid rgba(239, 241, 246, 1);
    }

    &-results {
      background-color: rgba(246, 248, 252, 1);

      &-wrap {
        background-color: rgba(246, 248, 252, 1);

        &:first-of-type {
          border-right: 1px solid rgba(223, 226, 236, 1)
        }
      }

      &-label {
        color: rgba(82, 90, 122, 1);
        font-size: 16px;
        font-weight: 500;
      }

      &-value {
        color: rgba(39, 44, 63, 1);
        font-size: 16px;
        font-weight: 600;

        &-green {
          color: rgba(255, 255, 255, 1);
          background-color: rgba(11, 161, 125, 1);
          border-radius: 6px;
          padding: 6px 12px;
        }
      }
    }

    &-input {
      flex-direction: row;
      margin-bottom: 0 !important;
    }

    &-label {
      color: rgba(82, 90, 122, 1);
      font-size: 11px;
      font-weight: 500;
    }
  }
}
</style>