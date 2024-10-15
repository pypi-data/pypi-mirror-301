<template>
  <div class="w-full h-full flex flex-col gap-2">
    <div class="w-full h-full flex gap-2">
      <div class="order-step bg-white w-6/12 border border-transparent rounded-md">
        <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
          <div class="order-step-header-name">Supplier Order</div>
        </div>
        <div class="order-step-content compliance-status w-full flex flex-col p-[0.75rem] gap-2">
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center">AML Buying Company</div>
            <div class="order-step-content-el-value py-[0.25rem] px-[0.75rem]">AML Global Limited</div>
          </div>
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center">Status</div>
            <div class="order-step-content-el-status py-[0.25rem] px-[0.75rem]">Approval required</div>
          </div>
        </div>
      </div>
      <div class="order-step bg-white w-6/12 border border-transparent rounded-md">
        <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
          <div class="order-step-header-name">Client Order</div>
        </div>
        <div class="order-step-content compliance-status w-full flex flex-col p-[0.75rem] gap-2">
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center">AML Selling Company</div>
            <div class="order-step-content-el-value py-[0.25rem] px-[0.75rem]">AML Global OU</div>
          </div>
          <div class="w-full flex gap-2">
            <div class="order-step-content-el-name flex items-center">Fuel Release</div>
            <div class="order-step-content-el-status-warn py-[0.25rem] px-[0.75rem]">Waiting on supplier confirmation
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="order-step bg-white w-full border border-transparent rounded-md"
      v-if="order?.fuel_order?.is_open_release">
      <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="order-step-header-name">Client Credit Exposure</div>
      </div>
      <div class="order-step-content w-full flex p-[0.75rem] gap-2">
        <CreditExposure :confirmed="mockCredit.confirmed" :limit="mockCredit.limit" :maximum="mockCredit.maximum"
          :open="mockCredit.open" :is-open-release="order?.fuel_order?.is_open_release" />
      </div>
    </div>
    <div class="order-step bg-white w-full border border-transparent rounded-md">
      <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="order-step-header-name">Uplifts</div>
      </div>
      <div class="order-step-content w-full flex flex-col" v-if="mockUplifts.length">
        <div class="order-step-content-header-wrap w-full flex items-center">
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Date & Time</div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Aircraft</div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Quantity Uplifted</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Destination</div>
          </div>
          <div class="order-step-content-col w-1/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Delivery Ticket</div>
          </div>
        </div>
        <div class="order-step-content-data-wrap selected-supplier w-full flex items-center"
          v-for="(uplift, index) in mockUplifts" :key="uplift.date">
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ uplift.date }}</div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ uplift.aircraft }}</div>
          </div>
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ uplift.quantity }}</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ uplift.destination }}</div>
          </div>
          <div class="order-step-content-col w-1/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
              <Button class="download-button"> <img width="20" height="20" src="../../assets/icons/download.svg"
                  alt="options" class="horizontal cursor-pointer"></Button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="order-step bg-white w-full border border-transparent rounded-md">
      <div class="order-step-header flex justify-between items-center py-[0.75rem] px-[0.75rem]">
        <div class="order-step-header-name">Client Documents</div>
        <div class="order-step-header-actions flex gap-4">
          <Button class="button flex items-center gap-2">
            <img src="../../assets/icons/plus.svg" alt="add">
            Add Document
          </Button>
        </div>
      </div>
      <div class="order-step-content w-full flex flex-col" v-if="mockDocuments.length">
        <div class="order-step-content-header-wrap w-full flex items-center">
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Type</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Name</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Entity</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Valid From</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">Valid To</div>
          </div>
          <div class="order-step-content-col w-1/12">
            <div class="order-step-content-col-header px-[0.75rem] py-[0.5rem]">&nbsp;</div>
          </div>
        </div>
        <div class="order-step-content-data-wrap selected-supplier w-full flex items-center"
          v-for="(document, index) in mockDocuments" :key="document.valid_from">
          <div class="order-step-content-col w-3/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ document.type }}</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ document.name }}</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ document.entity }}</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ document.valid_from }}</div>
          </div>
          <div class="order-step-content-col w-2/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">{{ document.valid_to }}</div>
          </div>
          <div class="order-step-content-col w-1/12">
            <div class="order-step-content-col-data px-[0.75rem] py-[0.5rem]">
              <Button class="download-button"> <img width="20" height="20" src="../../assets/icons/download.svg"
                  alt="options" class="horizontal cursor-pointer"></Button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="order-step bg-white w-full border border-transparent rounded-md"
      v-if="!order?.fuel_order?.is_open_release">
      <div class="order-step-header flex justify-between py-[1rem] px-[0.75rem]">
        <div class="order-step-header-name">Flight Tracking</div>
      </div>
      <div class="order-step-content w-full flex p-[0.75rem] gap-2">

      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { Button } from 'shared/components';
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

const mockCredit = ref({
  confirmed: 20000,
  open: 30000,
  maximum: 60000,
  limit: 100000,
})
const mockUplifts = ref([{
  date: new Date().toLocaleDateString('en-CA'),
  aircraft: '84-0001 (Beechcraft C-12U)',
  quantity: '5,221 Litres (Jet A1)',
  destination: 'International',
}])
const mockDocuments = ref([{
  type: 'Tax Registration Certificate',
  name: 'Proof of Tax Reg',
  entity: 'Luxaviation',
  valid_from: new Date().toLocaleDateString('en-CA'),
  valid_to: new Date().toLocaleDateString('en-CA'),
},
{
  type: 'AOC Ops Specification',
  name: 'Latest Ops Spec',
  entity: '84-0001 (Beechcraft C-12U)',
  valid_from: new Date().toLocaleDateString('en-CA'),
  valid_to: new Date().toLocaleDateString('en-CA'),
}])

const isLoadingOrder = ref(false);

const {
  data: orderStep,
  callFetch: fetchOrder,
} = useFetch<any, (order: any) => Promise<any>>(async (order: any) => {
  // const data = await OrderReferences.fetchSupplierFuelDetails(supplierId, detailsId)
  // console.log(data);
  isLoadingOrder.value = false;
  return []
  // return data;
})


watch(() => props.order, (order: IOrder) => {
  fetchOrder(order);
})

</script>

<style lang="scss">
.order-step {
  .button {
    background-color: rgba(81, 93, 138, 1) !important;
    color: white !important;
    font-weight: 500 !important;
    font-size: 16px !important;
    @apply flex shrink-0 focus:shadow-none mb-0 mt-0 p-2 px-[1rem] rounded-xl #{!important};
  }

  .download-button {
    background-color: rgba(240, 242, 252, 1);
    border-color: transparent;
    border-radius: 12px;
    box-shadow: none;
    padding: 10px;
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
        color: rgba(21, 28, 53, 1);
        font-size: 14px;
        font-weight: 500;
      }

      &-status {
        background-color: rgba(11, 161, 125, 1);
        color: rgb(255, 255, 255);
        border-radius: 6px;
        border: 1px solid transparent;
        font-size: 12px;
        font-weight: 500;
        text-transform: uppercase;

        &-warn {
          background-color: rgba(254, 161, 22, 1);
          color: rgb(255, 255, 255);
          border-radius: 6px;
          border: 1px solid transparent;
          font-size: 12px;
          font-weight: 500;
          text-transform: uppercase;

        }
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
        color: rgba(39, 44, 63, 1);
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
        .order-step-info-side {
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

      .order-step-info {
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


      .order-step-data {
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

  .compliance-credit {
    &-confirmed {
      &-value {
        border-left: 4px solid rgba(98, 132, 254, 1);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(98, 132, 254, 1);
        border-radius: 4px 0 0 4px;
      }
    }

    &-open {
      &-value {
        border-left: 4px solid rgba(243, 173, 43, 1);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(243, 173, 43, 1);
      }
    }

    &-maximum {
      &-value {
        border-left: 4px dashed rgba(243, 173, 43, 1);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background: repeating-linear-gradient(120deg,
            rgba(243, 173, 43, 1),
            rgba(243, 173, 43, 1) 1px,
            rgb(223, 243, 231) 0,
            rgb(223, 243, 231) 12px);
      }
    }

    &-remaining {
      &-value {
        border-left: 4px solid rgb(223, 243, 231);
        color: rgba(21, 28, 53, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgb(223, 243, 231);
      }
    }

    &-overuse {
      &-value {
        border-left: 4px solid rgba(254, 98, 98, 0.12);
        color: rgba(254, 98, 98, 1);
        font-size: 18px;
        font-weight: 600;

        &-name {
          color: rgba(82, 90, 122, 1);
          font-size: 12px;
          font-weight: 400;
        }
      }

      &-graph {
        height: 40px;
        width: 100%;
        background-color: rgba(254, 98, 98, 0.12);
        border-radius: 0 4px 4px 0;
      }
    }
  }
}
</style>