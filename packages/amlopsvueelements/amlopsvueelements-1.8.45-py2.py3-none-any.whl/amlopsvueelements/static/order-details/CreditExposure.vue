<template>
  <div class="credit-wrap flex w-full">
    <div class="credit-confirmed w-full flex flex-col gap-4" :style="{ 'width': calculateWidth(props.confirmed) }">
      <div class="credit-confirmed-graph"></div>
      <div class="credit-confirmed-value pl-[0.5rem]">
        <div class="credit-confirmed-value-name">Confirmed Fuel Uplift</div>
        {{ props.confirmed }}
      </div>
    </div>
    <div class="credit-open w-full flex flex-col gap-4" :style="{ 'width': calculateWidth(props.open) }">
      <div class="credit-open-graph"></div>
      <div class="credit-open-value pl-[0.5rem]">
        <div class="credit-open-value-name">Open Fuel Releases (Maximum)</div>
        {{ props.open }}
      </div>
    </div>
    <div class="credit-maximum w-full flex flex-col gap-4" :class="{ 'no-overuse': overuse === 0 }"
      :style="{ 'width': calculateWidth(props.maximum), 'display': props.isOpenRelease ? 'none' : 'flex' }">
      <div class="credit-maximum-graph"></div>
      <div class="credit-maximum-value pl-[0.5rem]">
        <div class="credit-maximum-value-name">Uplift Exposure (Maximum)</div>
        {{ props.maximum }}
      </div>
      <div class="credit-maximum-popup px-[0.75rem] py-[0.25rem]" v-if="overuse === 0 && !props.isOpenRelease">Total
        Credit
        Exposure (Maximum):
        <span>{{ use }}</span>
        <div class="credit-maximum-popup-line"></div>
        <div class="credit-maximum-popup-dot"></div>
      </div>
      <div class="credit-maximum-popup px-[0.75rem] py-[0.25rem]" v-else-if="!props.isOpenRelease">Credit Limit:
        <span>{{ props.limit }}</span>
        <div class="credit-maximum-popup-line"></div>
        <div class="credit-maximum-popup-dot"></div>
      </div>
    </div>
    <div class="credit-remaining w-full flex flex-col gap-4" v-if="overuse === 0"
      :style="{ 'width': calculateWidth(remaining) }">
      <div class="credit-remaining-graph"></div>
      <div class="credit-remaining-value pl-[0.5rem]">
        <div class="credit-remaining-value-name">Credit Remaining</div>
        {{ remaining }}
      </div>
      <div class="credit-remaining-popup px-[0.75rem] py-[0.25rem]">Credit Limit:
        <span>{{ props.limit }}</span>
        <div class="credit-remaining-popup-line"></div>
        <div class="credit-remaining-popup-dot"></div>
      </div>
    </div>
    <div class="credit-overuse w-full flex flex-col gap-4" v-else :style="{ 'width': calculateWidth(overuse) }">
      <div class="credit-overuse-graph"></div>
      <div class="credit-overuse-value pl-[0.5rem]">
        <div class="credit-overuse-value-name">Credit Overuse</div>
        {{ overuse }}
      </div>
      <div class="credit-overuse-popup px-[0.75rem] py-[0.25rem]">Total Credit Exposure (Maximum):
        <span>{{ capacity }}</span>
        <div class="credit-overuse-popup-line"></div>
        <div class="credit-overuse-popup-dot"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  confirmed: {
    type: Number,
    default: 0
  },
  open: {
    type: Number,
    default: 0
  },
  maximum: {
    type: Number,
    default: 0
  },
  limit: {
    type: Number,
    default: 0
  },
  isOpenRelease: Boolean
})

const use = computed(() => props.maximum + props.confirmed + props.open);
const overuse = computed(() => {
  const value = props.limit - (props.maximum + props.confirmed + props.open);
  return value > 0 ? 0 : Math.abs(value)
})
const capacity = computed(() => props.limit + overuse.value);
const remaining = computed(() => {
  const value = props.limit - (props.maximum + props.confirmed + props.open);
  return value > 0 ? value : 0
})

const calculateWidth = (value: number) => {
  const width = (value / capacity.value * 100);
  return width === 0 || width < 15 ? '15%' : width + '%';
}


</script>

<style lang="scss">
.credit {
  &-wrap {
    padding-top: 28px;
    background: rgb(245, 246, 249);
    border-radius: 4px 4px 0 0;
  }

  &-confirmed {
    background-color: rgb(255, 255, 255);

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
    background-color: rgb(255, 255, 255);

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
    background-color: rgb(255, 255, 255);
    position: relative;

    &-value {
      border-left: 4px dashed rgba(254, 98, 98, 1);
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
          rgba(254, 98, 98, 1),
          rgba(254, 98, 98, 1) 1px,
          rgb(223, 243, 231) 0,
          rgb(223, 243, 231) 12px);
    }

    &.no-overuse {
      .compliance-credit-maximum-value {
        border-left: 4px dashed rgba(243, 173, 43, 1);
      }

      .compliance-credit-maximum-graph {
        background: repeating-linear-gradient(120deg,
            rgba(243, 173, 43, 1),
            rgba(243, 173, 43, 1) 1px,
            rgb(223, 243, 231) 0,
            rgb(223, 243, 231) 12px);
      }
    }

    &-popup {
      width: max-content;
      position: absolute;
      right: 0;
      top: -14px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
      }

      &-line {
        position: absolute;
        width: 1px;
        right: -1px;
        height: 100%;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        z-index: 1;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 50px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-remaining {
    position: relative;
    background-color: rgb(255, 255, 255);

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
      width: calc(100% + 1px);
      background-color: rgb(223, 243, 231);
    }

    &-popup {
      position: absolute;
      width: max-content;
      right: -1px;
      top: -48px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
      }

      &-line {
        position: absolute;
        width: 1px;
        top: 28px;
        right: -1px;
        height: 59px;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 84px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }

  &-overuse {
    position: relative;
    background-color: rgb(255, 255, 255);

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
      width: calc(100% + 1px);
      background: repeating-linear-gradient(120deg,
          rgba(254, 98, 98, 1),
          rgba(254, 98, 98, 1) 1px,
          rgb(254, 236, 236) 0,
          rgb(254, 236, 236) 12px);
      background-color: rgba(254, 98, 98, 0.12);
      border-radius: 0 4px 4px 0;
    }

    &-popup {
      position: absolute;
      width: max-content;
      right: -1px;
      top: -48px;
      color: rgba(39, 44, 63, 1);
      font-size: 12px;
      font-weight: 400;
      background: rgba(255, 255, 255, 1);
      border: 1px solid rgba(139, 148, 178, 1);
      border-radius: 4px 4px 0px 4px;

      span {
        font-size: 14px;
        font-weight: 600;
        color: rgba(254, 98, 98, 1);
      }

      &-line {
        position: absolute;
        width: 1px;
        top: 28px;
        right: -1px;
        height: 59px;
        background-color: rgba(139, 148, 178, 1);
      }

      &-dot {
        position: absolute;
        width: 5px;
        right: -3px;
        height: 5px;
        top: 84px;
        border-radius: 50%;
        background-color: rgba(139, 148, 178, 1);
      }
    }
  }
}
</style>