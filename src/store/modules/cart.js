export default {
  namespaced: true,
  
  state: {
    items: []
  },
  
  mutations: {
    addItem(state, item) {
      const existingItem = state.items.find(i => i.id === item.id)
      if (existingItem) {
        existingItem.quantity++
      } else {
        state.items.push({ ...item, quantity: 1 })
      }
    },
    
    removeItem(state, itemId) {
      state.items = state.items.filter(item => item.id !== itemId)
    },
    
    updateItemQuantity(state, { id, quantity }) {
      const item = state.items.find(i => i.id === id)
      if (item) {
        item.quantity = quantity
      }
    },
    
    clearCart(state) {
      state.items = []
    }
  },
  
  getters: {
    itemCount: state => {
      return state.items.reduce((total, item) => total + item.quantity, 0)
    },
    
    totalPrice: state => {
      return state.items.reduce((total, item) => total + (item.price * item.quantity), 0)
    }
  }
} 