<template>
  <div class="dashboard">
    <h1>📦 Admin Dashboard</h1>

    <p v-if="message" class="message error">
      {{ message }}
    </p>

    <!-- Create Item -->
    <div class="form-card">
      <h2>Add New Item</h2>

      <form @submit.prevent="createItem">
        <input
          v-model="ItemDetails.name"
          type="text"
          placeholder="Item Name"
          required
        />

        <textarea
          v-model="ItemDetails.description"
          placeholder="Item Description"
        ></textarea>

        <input
          v-model="ItemDetails.image_url"
          type="text"
          placeholder="Image URL"
        />

        <button type="submit" class="create-btn">
          Create Item
        </button>
      </form>
    </div>

    <!-- Items -->
    <h2>Your Items</h2>

    <div class="items-grid">
      <div
        class="item-card"
        v-for="item in items"
        :key="item.id"
      >
        <img
          :src="item.image_url || 'https://placehold.co/400x300?text=No+Image'"
          class="item-image"
        />

        <div class="card-body">
          <h3>{{ item.name }}</h3>

          <p>{{ item.description }}</p>

          <div class="actions">
            <button
              class="edit-btn"
              @click="openEdit(item)"
            >
              ✏️ Edit
            </button>

            <button
              class="delete-btn"
              @click="DeleteItem(item.id)"
            >
              🗑 Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Edit Modal -->
    <div
      v-if="showEditModal"
      class="modal-overlay"
    >
      <div class="modal">
        <h2>Edit Item</h2>

        <input
          v-model="editItem.name"
          placeholder="Item Name"
        />

        <textarea
          v-model="editItem.description"
          placeholder="Description"
        ></textarea>

        <input
          v-model="editItem.image_url"
          placeholder="Image URL"
        />

        <div class="modal-buttons">
          <button
            class="save-btn"
            @click="updateItem"
          >
            Save
          </button>

          <button
            class="cancel-btn"
            @click="showEditModal=false"
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      message: "",

      items: [],

      ItemDetails: {
        name: "",
        description: "",
        image_url: ""
      },

      showEditModal: false,

      editItem: {
        id: null,
        name: "",
        description: "",
        image_url: ""
      }
    };
  },

  methods: {
    async createItem() {
      const res = await fetch("http://127.0.0.1:5000/items", {
        method: "POST",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify(this.ItemDetails)
      });

      const data = await res.json();

      if (res.ok) {
        alert("Item created!");

        this.ItemDetails = {
          name: "",
          description: "",
          image_url: ""
        };

        this.loadItems();
      } else if ([401, 403, 422].includes(res.status)) {
        localStorage.removeItem("token");
        this.$router.push("/login");
      } else {
        this.message = data.message;
      }
    },

    async loadItems() {
      const res = await fetch("http://127.0.0.1:5000/items", {
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      });

      const data = await res.json();

      if (res.ok) {
        this.items = data.items;
      } else if ([401, 422].includes(res.status)) {
        localStorage.removeItem("token");
        this.$router.push("/login");
      } else {
        this.message = data.message;
      }
    },

    async DeleteItem(id) {
      if (!confirm("Delete this item?")) return;

      const res = await fetch(`http://127.0.0.1:5000/items/${id}`, {
        method: "DELETE",
        headers: {
          Authorization: `Bearer ${localStorage.getItem("token")}`
        }
      });

      if (res.ok) {
        this.loadItems();
      } else if ([401, 403, 422].includes(res.status)) {
        localStorage.removeItem("token");
        this.$router.push("/login");
      }
    },

    openEdit(item) {
      this.editItem = { ...item };
      this.showEditModal = true;
    },

    async updateItem() {
      const res = await fetch(
        `http://127.0.0.1:5000/items/${this.editItem.id}`,
        {
          method: "PUT",
          headers: {
            Authorization: `Bearer ${localStorage.getItem("token")}`,
            "Content-Type": "application/json"
          },
          body: JSON.stringify(this.editItem)
        }
      );

      const data = await res.json();

      if (res.ok) {
        this.showEditModal = false;
        this.loadItems();
      } else {
        this.message = data.message;
      }
    }
  },

  mounted() {
    this.loadItems();
  }
};
</script>

<style scoped>
* {
  box-sizing: border-box;
}

.dashboard {
  max-width: 1200px;
  margin: auto;
  padding: 40px 20px;
  background: #f4f6fb;
  min-height: 100vh;
}

.dashboard h1 {
  text-align: center;
  margin-bottom: 30px;
  color: #222;
}

.form-card {
  background: white;
  padding: 25px;
  border-radius: 15px;
  box-shadow: 0 8px 20px rgba(0,0,0,.08);
  margin-bottom: 40px;
}

.form-card h2 {
  margin-bottom: 15px;
}

input,
textarea {
  width: 100%;
  padding: 12px;
  margin-bottom: 15px;
  border-radius: 8px;
  border: 1px solid #ddd;
  font-size: 15px;
}

textarea {
  min-height: 100px;
  resize: vertical;
}

input:focus,
textarea:focus {
  outline: none;
  border-color: #2563eb;
}

.create-btn {
  width: 100%;
  background: #2563eb;
  color: white;
  border: none;
  padding: 13px;
  border-radius: 8px;
  cursor: pointer;
  font-size: 16px;
}

.create-btn:hover {
  background: #1d4ed8;
}

.items-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px,1fr));
  gap: 25px;
  margin-top: 20px;
}

.item-card {
  background: white;
  border-radius: 15px;
  overflow: hidden;
  box-shadow: 0 8px 20px rgba(0,0,0,.08);
  transition: .3s;
}

.item-card:hover {
  transform: translateY(-6px);
}

.item-image {
  width: 100%;
  height: 220px;
  object-fit: cover;
}

.card-body {
  padding: 18px;
}

.card-body h3 {
  margin-bottom: 10px;
}

.card-body p {
  color: #666;
  min-height: 50px;
}

.actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}

.edit-btn,
.delete-btn,
.save-btn,
.cancel-btn {
  border: none;
  padding: 10px 18px;
  border-radius: 8px;
  cursor: pointer;
  color: white;
}

.edit-btn,
.save-btn {
  background: #2563eb;
}

.delete-btn {
  background: #dc2626;
}

.cancel-btn {
  background: gray;
}

.edit-btn:hover,
.save-btn:hover {
  background: #1d4ed8;
}

.delete-btn:hover {
  background: #b91c1c;
}

.cancel-btn:hover {
  background: #555;
}

.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: white;
  width: 420px;
  max-width: 90%;
  border-radius: 15px;
  padding: 25px;
}

.modal h2 {
  margin-bottom: 20px;
}

.modal-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.message {
  margin-bottom: 15px;
}

.error {
  color: red;
}
</style>