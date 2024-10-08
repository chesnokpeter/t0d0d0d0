<template>
<div class="container">
    <logo class="logo"></logo>
    <menu-comp sel="overview" class="menu"></menu-comp>
    <div class="content">
        <div class="inboxs">
            inbox //
            <div class="inbox"> <input class="calday-new" type="button" value="+" @click="addNewInbox()"> <div @click="openModal(inbox.name, inbox.project_id, inbox.date, inbox.time, inbox.status, inbox.id, undefined, 'inbox')" class="inbox-item" v-for="(inbox, index) in inboxs" :key="index" @dragstart="onDragStart($event, inbox)" @touchstart="onDragStart($event, inbox)" draggable="true">{{ inbox.name }}</div></div>
        </div>
        <div class="calendar-nav">
            <div class="backcal" @click="backcal"><</div>
            <div class="calendar-nav-title">// calendar //</div>
            <div class="backcal backcal2" @click="nextcal">></div>
        </div>
        <div class="calendar">
            <div class="calday" v-for="(c, i) in calendar" :key="i">
                <div class="calday-title">{{ c.dprint() }}</div>
                <div class="calday-tasks" @drop="onDrop($event, c.y_m_d())" @dragover.prevent @dragenter.prevent>
                    <div :class="['calday-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" v-for="(t, ii) in c.tasks" :key="ii" @click="openModal(t.name, t.project_id, t.date, t.time, t.status, t.id, i, 'task')" @dragstart="onDragStart($event, t)" draggable="true">
                        <div class="calday-task-title">{{ t.name }}</div>
                        <div class="calday-task-desc">
                            <div class="calday-task-project">{{ taskdescprint(t.project_name, t.time) }}</div>
                        </div>
                    </div>
                    <input class="calday-new" type="button" value="+" @click="addNewTask(c, i)">
                </div>
            </div>
        </div>
    </div>

    <ModalWindow v-if="showModal" @close="closeModal" :kind="kindModal" :id="idModal" :name="nameModal" :project="projectModal" :date="dateModal" :time="timeModal" :status="statusModal"/>

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

const nameModal = ref()
const projectModal = ref()
const dateModal = ref()
const timeModal = ref()
const statusModal = ref()
const idModal = ref()
const idCalday = ref()
const kindModal = ref()

function openModal(name, project, date, time, status, id, idc, kind) {
    nameModal.value = name
    projectModal.value = project
    dateModal.value = date
    timeModal.value = time
    showModal.value = true
    statusModal.value = status
    idModal.value = id
    idCalday.value = idc
    kindModal.value = kind
}

async function closeModal() {
    showModal.value = false

    if (kindModal.value == 'task') {
        let t = await gettasksbyid(idModal.value)
        if (t) {
            for (let i = 0; i < calendar.value.length; i++) {
                if (t.date == calendar.value[i].y_m_d()) {
                    const tt = await gettasksbydate(calendar.value[i].y_m_d())
                    calendar.value[i].setTasks(tt)
                }
                
            }
            if (t.date != calendar.value[idCalday.value].y_m_d()) {        
                t = await gettasksbydate(calendar.value[idCalday.value].y_m_d())
                calendar.value[idCalday.value].setTasks(t)
            }
        } else{
            t = await gettasksbydate(calendar.value[idCalday.value].y_m_d())
            calendar.value[idCalday.value].setTasks(t)
        }
    } else if (kindModal.value == 'inbox') {
        let t = await gettasksbyid(idModal.value)
        if (t) {
            for (let i = 0; i < inboxs.value.length; i++) {
                if (t.id == inboxs.value[i].id) {
                    inboxs.value[i] = t
                }
            }
        } else {
            for (let i = 0; i < inboxs.value.length; i++) {
                if (idModal.value == inboxs.value[i].id) {
                    inboxs.value.splice(i, 1)
                }
                
            }
        }
    }


}

async function gettasksbydate(date) {
    let r = await request('/task/get/byDate', 'POST', {date:date}, true)
    if (Object.keys(r.data[0]).length === 0) {
        return []
    }
    return r.data
}
async function gettasksbyid(data) {
    let r = await request('/task/get/byId', 'POST', {id:data}, true)
    return r.data[0]
}

async function backcal() {
    for (let i = 0; i < calendar.value.length; i++) {
        calendar.value[i].backDay()
        calendar.value[i].backDay()
        calendar.value[i].backDay()
        calendar.value[i].backDay()
        const t = await gettasksbydate(calendar.value[i].y_m_d())
        calendar.value[i].setTasks(t)
    }
    // calendar.value = [...calendar.value];
}

async function nextcal() {
    for (let i = 0; i < calendar.value.length; i++) {
        calendar.value[i].nextDay()
        calendar.value[i].nextDay()
        calendar.value[i].nextDay()
        calendar.value[i].nextDay()
        let t = await gettasksbydate(calendar.value[i].y_m_d())
        calendar.value[i].setTasks(t)
    }
    // calendar.value = [...calendar.value];
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

async function addNewTask(c, idc) {
    const r = await request('/task/new', 'POST', {name:'task', date:c.y_m_d()}, true)
    c.addTask(r.data[0])
    const task = r.data[0]
    nameModal.value = task.name
    projectModal.value = task.project
    dateModal.value = task.date
    timeModal.value = task.time
    showModal.value = true
    statusModal.value = task.status
    idModal.value = task.id
    idCalday.value = idc
    kindModal.value = 'task'
}

async function addNewInbox() {
    const r = await request('/task/new', 'POST', {name:'inbox'}, true)
    const task = r.data[0]
    nameModal.value = task.name
    projectModal.value = task.project
    dateModal.value = task.date
    timeModal.value = task.time
    showModal.value = true
    statusModal.value = task.status
    idModal.value = task.id
    kindModal.value = 'inbox'
    inboxs.value.push(task)
}

function onDragStart(e, task) {
    e.dataTransfer.dropEffect = 'move'
    e.dataTransfer.effectAllowed = 'move'
    e.dataTransfer.setData('task_id', task.id)
}

async function onDrop(e, date) {
    const task_id = e.dataTransfer.getData('task_id')

    for (let i = 0; i < inboxs.value.length; i++) {
        if (task_id == inboxs.value[i].id) {
            inboxs.value.splice(i, 1)
        }
        
    } for (let i = 0; i < calendar.value.length; i++) {
        for (let ii = 0; ii < calendar.value[i].tasks.length; ii++) {
            if (calendar.value[i].tasks[ii].id == task_id) {
                calendar.value[i].tasks.splice(ii, 1)
            }
        }
    }


    await request('/task/edit/date', 'PATCH', {id:task_id, edit:date}, true)
    for (let i = 0; i < calendar.value.length; i++) {
        if (date == calendar.value[i].y_m_d()) {
            const tt = await gettasksbydate(date)
            calendar.value[i].setTasks(tt)
        }
        
    }
}

onMounted(async ()=> {
    let r = await request('/inbox/get', 'GET', {}, true)
    for (let i = 0; i < r.data.length; i++) {
        inboxs.value.push(r.data[i])
    }

    let t = await gettasksbydate(today.y_m_d())
    calendar.value.push(reactive(new calday(today.y_m_d(), t)))
    today.nextDay()
    t = await gettasksbydate(today.y_m_d())
    calendar.value.push(reactive(new calday(today.y_m_d(), t)))
    today.nextDay()
    t = await gettasksbydate(today.y_m_d())
    calendar.value.push(reactive(new calday(today.y_m_d(), t)))
    today.nextDay()
    t = await gettasksbydate(today.y_m_d())
    calendar.value.push(reactive(new calday(today.y_m_d(), t)))
    today.nextDay()

})

</script>

<style>
#app{
    align-items: center;
}
body{
    overflow-x: hidden;
}

</style>

<style scoped lang="scss">
.content{
    margin-left: 150px;
    
}


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
    padding: 0px;
}

* {
    box-sizing: border-box;
}

.container {
    position: relative;
    margin-top: 100px; 
    width: 100%;
}

.logo {
    display: flex;

    width: 100%; 
    /* height: 100%; */
    margin: 0 auto;
}

.menu {
    position: absolute;
    left: 50px;
}

.inbox {
    max-width: 1000px;
    display: flex;
    flex-wrap: wrap;
}

.calendar {
    display: flex;
    justify-content: space-between;
    max-width: 1000px;
}

.calday, .calday-tasks {
    display: flex;
    flex-direction: column;
    gap: 10px;

}

.calday {
    min-width: 150px;
}

.calday-task {
    max-width: 150px;
    // white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    position: relative;
    border: var(--gray-color) solid 1px;
    &.isdonetask{
        border: var(--green-color) solid 1px;
        background-color: var(--green-color);
        color: var(--black-color);
    }
    &.isstoptask{
        border: var(--red-color) solid 1px;
    }
}


.inbox-item:hover{
    background-color: var(--white-color);
    color: var(--black-color);
}

.calday-task:hover{
    background-color: var(--white-color);
    color: var(--black-color);
    border: var(--white-color) solid 1px;
    overflow: visible;
    &.isdonetask{
        background-color: var(--black-color);
        color: var(--green-color);
        border: var(--green-color) solid 1px;
    }
    &.isstoptask{
        background-color: var(--red-color);
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

.calendar-nav {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    max-width: 1000px;
}

.calendar-nav-title {
    color: var(--gray-color);
}

.backcal {
    flex: 1;
}

.backcal:hover{
    background-color: var(--gray-color);
    color: var(--black-color);
}

.backcal2 {
    text-align: end;
}

input{
    border-color: none;
    background-color: var(--black-color);
    border: none;
    color: var(--white-color);
    font-family: "Source Code Pro", monospace;
    font-size: 16px;
}

input:hover{
    background-color: var(--gray-color);
    color: var(--black-color);
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
    }.content {
        margin: 0;
    }

}


</style>