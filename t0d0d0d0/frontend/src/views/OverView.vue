<template>
<div class="container">
    <logo class="logo"></logo>
    <menu-comp sel="overview" class="menu"></menu-comp>
    <div class="content">
        <div class="inboxs">
            inbox //
            <div class="inbox"><div class="inbox-item" v-for="(inbox, index) in inboxs" :key="index">{{ inbox }}</div></div>
        </div>
        <div class="calendar">
            <div class="calday" v-for="(c, i) in calendar" :key="i">
                <div class="calday-title">{{ c.dprint() }}</div>
                    <div class="calday-tasks">
                        <div :class="['calday-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" v-for="(t, i) in c.tasks" :key="i" @click="openModel(t.name, t.project_name, t.date, t.time)">
                            <div class="calday-task-title">{{ t.name }}</div>
                            <div class="calday-task-desc">
                                <div class="calday-task-project">{{ taskdescprint(t.project_name, t.time) }}</div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        <div class="backcal" @click="backcal"><</div>
        <div class="backcal" @click="nextcal">></div>
    </div>

    <!-- <button @click="showModal = true">Open Modal</button> -->
    <ModalWindow v-if="showModal" @close="showModal = false" kind="task" :name="nameModel" :project="projectModel" :date="dateModel" :time="timeModel"/>

</div>
</template>


<script setup>
import Logo from '../components/Logo.vue'
import { request } from '@/modules/requester'
import { calday } from '@/modules/calday'
import MenuComp from '../components/MenuComp.vue'
import { onMounted, ref, reactive } from 'vue';
import ModalWindow from '@/components/ModalWindow.vue';

const inboxs = ref([])
const today = new calday(todaydate())
const calendar = ref([])
const showModal = ref(false)

const nameModel = ref()
const projectModel = ref()
const dateModel = ref()
const timeModel = ref()

function openModel(name, project, date, time) {
    nameModel.value = name
    projectModel.value = project
    dateModel.value = date
    timeModel.value = time
    showModal.value = true
}


async function gettasksbydate(date) {
    let r = await request('/task/getTaskByDate', 'POST', {date:date}, true)
    return r.data
}
async function backcal() {
    for (let i = 0; i < calendar.value.length; i++) {
        calendar.value[i].backDay()
        calendar.value[i].backDay()
        calendar.value[i].backDay()
        let t = await gettasksbydate(calendar.value[i].y_m_d())
        calendar.value[i].setTasks(t)
    }
    calendar.value = [...calendar.value];
}

async function nextcal() {
    for (let i = 0; i < calendar.value.length; i++) {
        calendar.value[i].nextDay()
        calendar.value[i].nextDay()
        calendar.value[i].nextDay()
        let t = await gettasksbydate(calendar.value[i].y_m_d())
        calendar.value[i].setTasks(t)
    }
    calendar.value = [...calendar.value];
}

function isdonetask(task) {
    if (task.status == 'done') {
        return true
    } return false
}

function isstoptask(task) {
    if (task.status == 'stop') {
        return true
    } return false
}

function todaydate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`
}

function taskdescprint(project, time) {
    if (project && time) {
        return `${project} - ${time}`
    } return project
}

onMounted(async ()=> {
    let r = await request('/task/getInbox', 'GET', {}, true)
    for (let i = 0; i < r.data.length; i++) {
        inboxs.value.push(r.data[i].name)
    }

    let ts = await gettasksbydate(today.y_m_d())
    calendar.value.push(reactive(new calday(today.y_m_d(), ts)))
    today.nextDay()
    ts = await gettasksbydate(today.y_m_d())
    calendar.value.push(reactive(new calday(today.y_m_d(), ts)))
    today.nextDay()
    ts = await gettasksbydate(today.y_m_d())
    calendar.value.push(reactive(new calday(today.y_m_d(), ts)))

})

</script>

<style>
#app{
    align-items: center;
}

</style>

<style scoped lang="scss">
.inboxs {
    display: flex;
    flex-direction: column;
    color: var(--gray-color);
    gap: 10px;
}

.inbox {
    display: flex;
    /* flex-direction: column; */
    color: var(--white-color);
    gap: 10px;
    }
.inbox-item {
    outline:1px solid var(--gray-color);
    outline-offset:-1px;
    padding: 3.5px;
}

* {
    box-sizing: border-box;
}

.container {
    position: relative;
    margin-top: 150px; 
}

.logo {
    display: block;
    width: 100%; 
    /* height: 100%; */
    margin: 0 auto;
}

.menu {
    position: absolute;
    left: -100px;
}

.inbox {
    max-width: 600px;
    display: flex;
    flex-wrap: wrap;
}

.calendar {
    display: flex;
    justify-content: space-between;
}

.calday, .calday-tasks {
    display: flex;
    flex-direction: column;
    gap: 15px;
}

.calday-task {
    border: var(--gray-color) solid 1px;
    &.isdonetask{
        border: var(--green-color) solid 1px;
    }
    &.isstoptask{
        border: var(--red-color) solid 1px;
    }
}

.calday-title {
    text-decoration: underline ;
    color: var(--gray-color);
}

.calday-task-title {
    font-size: 16px;
}

.calday-task-desc {
    font-size: 12px;
}

@media (max-width: 750px) {
    .container {
        margin-top: 0px; 
    }
    .logo {
        width: 100%; 
        position: sticky;
        top: 0;
    }
    .menu {
        position: fixed;
        bottom: 0;
        width: 100%;
        left: 0;
        flex-direction: row;
        justify-content: space-between;
    }

}

</style>