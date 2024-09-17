<template>
    <div class="container">
        <logo class="logo"></logo>
        <menu-comp sel="tasks" class="menu"></menu-comp>
        <div class="content">
            <div class="day-picker">
                <div class="day-left" @click="day_left"><</div>
                <div class="day-status">{{ today[0].dprint() }}</div>
                <div class="day-right" @click="day_right">></div>
            </div>
            <div class="titles">
                <div class="title">backlog</div>
                <div class="title">done</div>
                <div class="title">stop</div>
            </div>
            <div class="taskmanager">
                <div class="taskgroup">
                    <div :class="['one-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" @click="openModal(t.name, t.project_id, t.date, t.time, t.status, t.id, i, 'task')" v-for="(t, i) in today[0]?.tasks?.filter(task => task.status == 'backlog')" :key="i" >
                        {{ t.name }}
                    </div> 
                </div>
                <div class="taskgroup">
                    <div :class="['one-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" @click="openModal(t.name, t.project_id, t.date, t.time, t.status, t.id, i, 'task')" v-for="(t, i) in today[0]?.tasks?.filter(task => task.status == 'done')" :key="i" >
                        {{ t.name }}
                    </div> 
                </div>
                <div class="taskgroup">
                    <div :class="['one-task',{'isdonetask': isdonetask(t), 'isstoptask':isstoptask(t)}]" @click="openModal(t.name, t.project_id, t.date, t.time, t.status, t.id, i, 'task')" v-for="(t, i) in today[0]?.tasks?.filter(task => task.status == 'stop')" :key="i" >
                        {{ t.name }}
                    </div> 
                </div>
            </div>
        </div>
    </div>

    <ModalWindow v-if="showModal" @close="closeModal" :kind="kindModal" :id="idModal" :name="nameModal" :project="projectModal" :date="dateModal" :time="timeModal" :status="statusModal"/>

</template>


<script setup>
import Logo from '../components/Logo.vue'
import { request } from '@/modules/requester'
import MenuComp from '../components/MenuComp.vue'
import { onMounted, ref } from 'vue';
import { calday } from '@/modules/calday'
import ModalWindow from '@/components/ModalWindow.vue';

'.'

const today = ref([new calday(todaydate())])

const showModal = ref(false)

const nameModal = ref()
const projectModal = ref()
const dateModal = ref()
const timeModal = ref()
const statusModal = ref()
const idModal = ref()
const idCalday = ref()
const kindModal = ref()

function todaydate() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    return `${year}-${month}-${day}`
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
        // let t = await gettasksbyid(idModal.value)
        // if (t) {
        //     for (let i = 0; i < calendar.value.length; i++) {
        //         if (t.date == calendar.value[i].y_m_d()) {
        //             const tt = await gettasksbydate(calendar.value[i].y_m_d())
        //             calendar.value[i].setTasks(tt)
        //         }
                
        //     }
        //     if (t.date != calendar.value[idCalday.value].y_m_d()) {        
        //         t = await gettasksbydate(calendar.value[idCalday.value].y_m_d())
        //         calendar.value[idCalday.value].setTasks(t)
        //     }
        // } else{
        //     t = await gettasksbydate(calendar.value[idCalday.value].y_m_d())
        //     calendar.value[idCalday.value].setTasks(t)
        // }
        let t = await gettasksbydate(today.value[0].y_m_d())
        today.value[0].setTasks(t)
    } 


}


async function gettasksbydate(date) {
    let r = await request('/task/get/byDate', 'POST', {date:date}, true)
    if (Object.keys(r.data[0]).length === 0) {
        return []
    }
    return r.data
}

async function day_left() {
    today.value[0].backDay()
    let t = await gettasksbydate(today.value[0].y_m_d())
    today.value[0].setTasks(t)
}

async function day_right() {
    today.value[0].nextDay()
    let t = await gettasksbydate(today.value[0].y_m_d())
    today.value[0].setTasks(t)
}

onMounted(async ()=> {
    let t = await gettasksbydate(today.value[0].y_m_d())
    today.value[0].setTasks(t)
    
})



</script>

<style>
#app{
    align-items: center;
}
</style>

<style scoped lang="scss">
.day-picker{
    display: inline-flex;
    gap: 10px;
    border: var(--gray-color) solid 1px;
}

.one-task {
    max-width: 150px;
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

.title {
    min-width: 150px;
}

.titles{
    display: flex;
    justify-content: space-between;
    max-width: 1000px;
    background-color: var(--white-color);
    color: var(--black-color);
    margin-top: 10px;
}

.content{
    margin-left: 150px;
}

.one-task{
    max-width: 150px;
}

.taskgroup-title{
    background-color: var(--white-color);
    color: var(--black-color);
}

.taskgroup{
    display: flex;
    flex-direction: column;
    gap: 10px;
    min-width: 150px;
}


.taskmanager{
    display: flex;
    justify-content: space-between;
    max-width: 1000px;
    margin-top: 10px;
}

.menu {
    position: absolute;
    left: 50px;
}

.container {
    position: relative;
    margin-top: 100px; 
    width: 100%;
}

.logo {
    display: flex;
    width: 100%; 
    margin: 0 auto;
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