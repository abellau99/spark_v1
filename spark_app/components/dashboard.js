// components/Dashboard.js

import React from 'react';

const Dashboard = () => {
  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Dashboard</h1>
      <div className="grid grid-cols-2 gap-4">
        <button className="bg-blue-500 text-white p-4 rounded hover:bg-blue-600">
          Button 1
        </button>
        <button className="bg-green-500 text-white p-4 rounded hover:bg-green-600">
          Button 2
        </button>
        {/* Add more buttons as needed */}
      </div>
    </div>
  );
};

export default Dashboard;
