/**
 * API service for communicating with the backend
 */
import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API Error:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

/**
 * Order API endpoints
 */
export const orderAPI = {
  /**
   * Get all orders
   */
  getAllOrders: async () => {
    try {
      const response = await api.get('/orders');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch orders');
    }
  },

  /**
   * Get order by ID
   */
  getOrderById: async (orderId) => {
    try {
      const response = await api.get(`/orders/${orderId}`);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch order');
    }
  },

  /**
   * Create new order
   */
  createOrder: async (orderData) => {
    try {
      const response = await api.post('/orders', orderData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to create order');
    }
  },

  /**
   * Update order
   */
  updateOrder: async (orderId, orderData) => {
    try {
      const response = await api.put(`/orders/${orderId}`, orderData);
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to update order');
    }
  },

  /**
   * Delete order
   */
  deleteOrder: async (orderId) => {
    try {
      await api.delete(`/orders/${orderId}`);
      return true;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to delete order');
    }
  },
};

/**
 * Product API endpoints
 */
export const productAPI = {
  /**
   * Get all products
   */
  getAllProducts: async () => {
    try {
      const response = await api.get('/products');
      return response.data;
    } catch (error) {
      throw new Error(error.response?.data?.detail || 'Failed to fetch products');
    }
  },
};

export default api;

