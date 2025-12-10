/**
 * Main App Component
 * Manages the order management application state and routing
 */
import { useState } from 'react';
import OrderList from './components/OrderList';
import OrderForm from './components/OrderForm';
import './App.css';

function App() {
  const [view, setView] = useState('list'); // 'list' or 'form'
  const [selectedOrder, setSelectedOrder] = useState(null);

  const handleAddOrder = () => {
    setSelectedOrder(null);
    setView('form');
  };

  const handleEditOrder = (order) => {
    setSelectedOrder(order);
    setView('form');
  };

  const handleCancel = () => {
    setSelectedOrder(null);
    setView('list');
  };

  const handleSuccess = () => {
    setSelectedOrder(null);
    setView('list');
  };

  return (
    <div className="app">
      {view === 'list' ? (
        <OrderList onAddOrder={handleAddOrder} onEditOrder={handleEditOrder} />
      ) : (
        <OrderForm
          order={selectedOrder}
          onCancel={handleCancel}
          onSuccess={handleSuccess}
        />
      )}
    </div>
  );
}

export default App;
