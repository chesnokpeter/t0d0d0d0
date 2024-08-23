


export class calday {
    constructor(dateString, tasks) {
        const ds = dateString.split("-");
        this.year = parseInt(ds[0])
        this.month = parseInt(ds[1])
        this.day = parseInt(ds[2])
        this.tasks = tasks
    }

    y_m_d(){
        let month = String(this.month)
        let day = String(this.day)
        let year = String(this.year)
        if (month.length == 1) {
            month = `0${month}`
        }
        if (day.length == 1) {
            day = `0${day}`
        }
        return `${year}-${month}-${day}`
    }

    dprint() {
        const m = ['', 'jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        return `${this.day} ${m[this.month]}`
    }

    isLeapYear(year){
        if (year % 4 === 0) {
            if (year % 100 === 0) {
                if (year % 400 === 0) {
                    return true;
                } else {
                    return false;
                }
            } else {
                return true;
            }
        } else {
            return false;
        }
    }

    maxDaysMonth(){
        const m31d = [1, 3, 5, 7, 8, 10, 12]
        const m30d = [4, 6, 9, 11]

        for (let i = 0; i < m31d.length; i++) {
            if (m31d[i] == this.month) {
                return 31
            }
        }
        for (let i = 0; i < m30d.length; i++) {
            if (m30d[i] == this.month) {
                return 30
            }
        }
        if (this.month == 2) {
            if (this.isLeapYear(this.year)) {
                return 29
            } return 28
        }
    }

    nextDay(){
        if (this.day == this.maxDaysMonth()) {
            if (this.month == 12) {
                this.year = this.year + 1
                this.month = 1
                this.day = 1
            } else {
                this.month = this.month + 1
                this.day = 1
            }
        } else {
            this.day = this.day + 1
        }
    }

    backDay(){
        if (this.day == 1) {
            if (this.month == 1) {
                this.year = this.year - 1
                this.month = 12
                this.day = 31
            } else {
                this.month = this.month - 1
                this.day = this.maxDaysMonth()
            }
        } else {
            this.day = this.day - 1
        } 
    }

    setTasks(tasks){
        this.tasks = tasks
    }

    addTask(task){
        this.tasks.push(task)
    }
}


