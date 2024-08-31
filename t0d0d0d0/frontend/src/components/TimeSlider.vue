<template>
    <div class="time-slider">
    <div class="slider">
        <div class="slider-items">
        <div
            v-for="(option, index) in hours"
            :key="index"
            :class="['item', { 'active': index === selectedHour }]"
            @click="selectHour(index)"
        >
            {{ option }}
        </div>
        </div>
    </div>
    <div class="separator">:</div>
    <div class="slider">
        <div class="slider-items">
        <div
            v-for="(option, index) in minutes"
            :key="index"
            :class="['item', { 'active': index === selectedMinute }]"
            @click="selectMinute(index)"
        >
            {{ option }}
        </div>
        </div>
    </div>
    <div class="separator">:</div>
    <div class="slider">
        <div class="slider-items">
        <div
            v-for="(option, index) in seconds"
            :key="index"
            :class="['item', { 'active': index === selectedSecond }]"
            @click="selectSecond(index)"
        >
            {{ option }}
        </div>
        </div>
    </div>
    </div>
</template>

<script>


import { ref, defineComponent } from 'vue';

export default defineComponent({
    name: 'TimeSlider',

    setup(_){
        const hours = Array.from({ length: 24 }, (_, i) => i.toString().padStart(2, '0'));
        const minutes = Array.from({ length: 60 }, (_, i) => i.toString().padStart(2, '0'));
        const seconds = Array.from({ length: 60 }, (_, i) => i.toString().padStart(2, '0'));

        const selectedHour = ref(0);
        const selectedMinute = ref(0);
        const selectedSecond = ref(0);

        const selectHour = (index) => {selectedHour.value = index;};

        const selectMinute = (index) => {selectedMinute.value = index;};

        const selectSecond = (index) => {selectedSecond.value = index;};

        return { hours, minutes, seconds, selectHour, selectMinute, selectSecond, selectedHour, selectedMinute, selectedSecond }
    }
})

</script>

<style scoped>
.time-slider {
display: flex;
align-items: center;
justify-content: center;
}

.slider {
width: 60px;
height: 150px;
overflow: hidden;
position: relative;
text-align: center;
border-radius: 10px;
box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
background-color: #f5f5f5;
}

.separator {
font-size: 2rem;
margin: 0 10px;
}

.slider-items {
display: flex;
flex-direction: column;
align-items: center;
transition: transform 0.3s ease;
position: absolute;
width: 100%;
top: 50%;
transform: translateY(-50%);
}

.item {
padding: 15px 0;
font-size: 1.5rem;
color: #aaa;
cursor: pointer;
}

.item.active {
color: #000;
font-weight: bold;
font-size: 2rem;
}
</style>