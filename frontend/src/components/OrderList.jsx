/**
 * OrderList Component - Displays list of orders with search functionality
 */
import { useState, useEffect } from 'react';
import { orderAPI } from '../services/api';
import './OrderList.css';

const OrderList = ({ onAddOrder, onEditOrder }) => {
  const [orders, setOrders] = useState([]);
  const [filteredOrders, setFilteredOrders] = useState([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Fetch orders on component mount
  useEffect(() => {
    fetchOrders();
  }, []);

  // Filter orders when search term changes
  useEffect(() => {
    filterOrders();
  }, [searchTerm, orders]);

  const fetchOrders = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await orderAPI.getAllOrders();
      setOrders(data);
      setFilteredOrders(data);
    } catch (err) {
      setError(err.message);
      console.error('Error fetching orders:', err);
    } finally {
      setLoading(false);
    }
  };

  const filterOrders = () => {
    if (!searchTerm.trim()) {
      setFilteredOrders(orders);
      return;
    }

    const term = searchTerm.toLowerCase();
    const filtered = orders.filter(
      (order) =>
        order.id.toString().includes(term) ||
        order.order_description.toLowerCase().includes(term)
    );
    setFilteredOrders(filtered);
  };

  const handleDelete = async (orderId) => {
    if (!window.confirm('Are you sure you want to delete this order?')) {
      return;
    }

    try {
      await orderAPI.deleteOrder(orderId);
      await fetchOrders(); // Refresh the list
    } catch (err) {
      alert(`Error deleting order: ${err.message}`);
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  if (loading) {
    return <div className="loading">Loading orders...</div>;
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error">Error: {error}</p>
        <button onClick={fetchOrders} className="btn btn-primary">
          Retry
        </button>
      </div>
    );
  }

  return (
    <div className="order-list-container">
      <div className="header">
        <h1>Order Management</h1>
        <button onClick={onAddOrder} className="btn btn-primary">
          + Add New Order
        </button>
      </div>

      <div className="search-container">
        <input
          type="text"
          placeholder="Search by Order ID or Description..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="search-input"
        />
      </div>

      {filteredOrders.length === 0 ? (
        <div className="no-orders">
          <p>{searchTerm ? 'No orders found matching your search.' : 'No orders yet. Create your first order!'}</p>
        </div>
      ) : (
        <div className="table-container">
          <table className="orders-table">
            <thead>
              <tr>
                <th>Order ID</th>
                <th>Description</th>
                <th>Count of Products</th>
                <th>Products</th>
                <th>Created At</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {filteredOrders.map((order) => (
                <tr key={order.id}>
                  <td>#{order.id}</td>
                  <td>{order.order_description}</td>
                  <td className="product-count">{order.products.length}</td>
                  <td>
                    <div className="products-list">
                      {order.products.map((product, index) => (
                        <span key={product.id} className="product-tag">
                          {product.product_name}
                          {index < order.products.length - 1 && ', '}
                        </span>
                      ))}
                    </div>
                  </td>
                  <td>{formatDate(order.created_at)}</td>
                  <td>
                    <div className="action-buttons">
                      <button
                        onClick={() => onEditOrder(order)}
                        className="btn btn-secondary btn-sm"
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(order.id)}
                        className="btn btn-danger btn-sm"
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
};

export default OrderList;

