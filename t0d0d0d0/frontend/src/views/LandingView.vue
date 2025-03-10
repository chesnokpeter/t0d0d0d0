<template>
    <div class="menu">
        <div class="box">
            <router-link to="/signup">sign up</router-link>
        </div>
        <div class="box">
            <router-link to="/login">log in</router-link>
        </div>
    </div>


    <div class="logo-wrapper top90">
        <img src="../assets/shadowt0.svg.svg" alt="" class="logo" id="logo">
    </div>
    <div class="header">Take Control of Your Tasks with the Ultimate Todo Manager</div>
    <div class="description organize">Organize, Prioritize, and Conquer Your Day – All in One Place</div>
    <img src="../assets/bigfeatures.svg" alt="" class="features top90">
    <div class="description top90">Available Everywhere</div>
    <img src="../assets/anywhere.svg" alt="" class="anywhere top90">
    <div class="description top90">Open Code – Open Opportunities</div>
    <div class="descdesc">We believe that the best tools are created by the community. That`s why our Todo Manager is an open-source project</div>
    <a href="https://github.com/chesnokpeter/t0d0d0d0" class="link">https://github.com/chesnokpeter/t0d0d0d0</a>
    <div class="top90 ofna">t0d0d0d0 OFNA (Open. Free. NoAds) © 2025</div>
    <div class="top90 empty">t0d0d0d</div>
</template>

    
<script setup>

import { RouterLink } from 'vue-router'


</script>


<style scoped lang="scss">

a {
    text-decoration: none;
    color: var(--white-color);
}

.header {
    font-size: 2.8vw;
}

.description {
    font-size: 28px;
}

.box {
    font-size: 16px;
    padding: 10px;
    box-shadow: 10px 10px 0px 0px rgba(0, 0, 0, 1);
    border: var(--white-color) solid 1px;
    transition: .2s;
}

.box:hover {
    box-shadow: none;
}

.menu {
    display: flex;
    position: fixed;
    right: 60px;
    top: 30px;
    gap: 30px;
    box-shadow: 0px 0px 0px 2000px rgba(0, 0, 0, 1);
    background-color: #000;
    animation: postLoad 0.5s 0.5s forwards; 
}

.top90 {
    margin-top: 90px;
}

.descdesc {
    color: #888888;
    font-size: 20px;
    max-width: 45vw;
}

.link {
    font-size: 20px;
    color: var(--blue-color);
}


.empty {
    color: #121212;
}


@media (max-width: 1154px) {
    .features {
        content: url('../assets/smallfeatures.svg');
    }
    .anywhere {
        content: url('../assets/smallanywhere.svg');
    }

    .logo {
        width: 100%;
    }

    .organize {
        display: none;
    }

    .description {
        font-size: 28px;
        margin-left: 20px;
    }

    .header {
        font-size: 30px;
        margin-left: 20px;
    }

    .descdesc {
        font-size: 14px;
        max-width: none;
        margin-left: 20px;
    }

    .link {
        font-size: 14px;
    }

    .top90 {
        margin-top: 45px;
    }

    .descdesc {
        margin-top: 20px;
    }

    .logo-wrapper {
        margin-top: 90px;
    }
}



@keyframes postLoad {
    from {
        box-shadow: 0px 0px 0px 2000px rgba(0, 0, 0, 1);
    }
    to {
        box-shadow: none;
        background-color: #121212;
    }
}




</style>