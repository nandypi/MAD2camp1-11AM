<template>
    <div style="display: flex; justify-content: space-between;">
        <h1>User Dashboard</h1>
        <button @click="LogOut">Logout</button>
    </div>
    
    <p v-if="message" style="color: red;">{{ message }}</p>

    <div>
        <ul>
            <li v-for="item in items">
                <div>
                    <h3>{{ item.name }}</h3>
                    <p>{{ item.description }}</p>
                    <img :src="item.image_url" alt="" style="width: 150px;">
                </div>
            </li>
        </ul>
    </div>

</template>

<script>

export default {
    data() {
        return {
            message: '',
            items: []
        }
    },
    methods: {
        async loadItems() {
            const res = await fetch('http://127.0.0.1:5000/items', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('token')}`
                }
            })
            const data = await res.json()
            console.log(data)
            if (res.ok) {
                console.log('ok response');
                this.items = data.items
            } else if ([401, 422].includes(res.status)) {
                localStorage.removeItem('token')
                localStorage.removeItem('user')
                this.$router.push('/login');
            } else {
                this.message = data.message
            }
        },
        LogOut() {
            if (confirm("Are you sure about logging out?")) {
                localStorage.removeItem('user')
                localStorage.removeItem('token')
                this.$router.push('/login')
            }
        }
    },
    mounted() {
        console.log('component mounted')
        this.loadItems()
    }
}
</script>