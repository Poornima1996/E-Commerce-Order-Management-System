/**
 * OrderForm Component - Form for creating/editing orders
 */
import { useState, useEffect } from 'react';
import { orderAPI, productAPI } from '../services/api';
import './OrderForm.css';

const OrderForm = ({ order, onCancel, onSuccess }) => {
  const [formData, setFormData] = useState({
    order_description: '',
    product_ids: []
  });
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [loadingProducts, setLoadingProducts] = useState(true);

  const isEditMode = !!order;

  // Fetch products on component mount
  useEffect(() => {
    fetchProducts();
  }, []);

  // Populate form when editing
  useEffect(() => {
    if (order) {
      setFormData({
        order_description: order.order_description,
        product_ids: order.products.map(p => p.id)
      });
    }
  }, [order]);

  const fetchProducts = async () => {
    try {
      setLoadingProducts(true);
      const data = await productAPI.getAllProducts();
      setProducts(data);
    } catch (err) {
      setError(`Failed to load products: ${err.message}`);
    } finally {
      setLoadingProducts(false);
    }
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleProductToggle = (productId) => {
    setFormData((prev) => {
      const isSelected = prev.product_ids.includes(productId);
      return {
        ...prev,
        product_ids: isSelected
          ? prev.product_ids.filter(id => id !== productId)
          : [...prev.product_ids, productId]
      };
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Validation
    if (!formData.order_description.trim()) {
      setError('Order description is required');
      return;
    }

    if (formData.product_ids.length === 0) {
      setError('Please select at least one product');
      return;
    }

    try {
      setLoading(true);
      setError(null);

      const orderData = {
        order_description: formData.order_description,
        product_ids: formData.product_ids
      };

      if (isEditMode) {
        await orderAPI.updateOrder(order.id, orderData);
      } else {
        await orderAPI.createOrder(orderData);
      }

      onSuccess();
    } catch (err) {
      setError(err.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  if (loadingProducts) {
    return <div className="loading">Loading products...</div>;
  }

  return (
    <div className="order-form-container">
      <div className="form-header">
        <h2>{isEditMode ? 'Edit Order' : 'Book New Order'}</h2>
      </div>

      {error && (
        <div className="error-message">
          {error}
        </div>
      )}

      <form onSubmit={handleSubmit} className="order-form">
        <div className="form-group">
          <label htmlFor="order_description">
            Order Description <span className="required">*</span>
          </label>
          <input
            type="text"
            id="order_description"
            name="order_description"
            value={formData.order_description}
            onChange={handleInputChange}
            placeholder="Enter order description"
            maxLength={100}
            required
            className="form-input"
          />
        </div>

        <div className="form-group">
          <label>
            Select Products <span className="required">*</span>
          </label>
          <div className="products-grid">
            {products.map((product) => {
              const isSelected = formData.product_ids.includes(product.id);

              return (
                <div key={product.id} className="product-checkbox">
                  <label>
                    <input
                      type="checkbox"
                      checked={isSelected}
                      onChange={() => handleProductToggle(product.id)}
                    />
                    <div className="product-info">
                      <span className="product-name">{product.product_name}</span>
                      <span className="product-description">
                        {product.product_description}
                      </span>
                    </div>
                  </label>
                </div>
              );
            })}
          </div>
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={onCancel}
            className="btn btn-secondary"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Saving...' : isEditMode ? 'Update Order' : 'Book Order'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default OrderForm;

