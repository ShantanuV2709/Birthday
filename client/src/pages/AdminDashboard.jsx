import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Users, Baby, Calculator, DollarSign, LogOut, Loader2, RefreshCw } from 'lucide-react';
import { useNavigate } from 'react-router-dom';
import { guestApi } from '../api';

const AdminDashboard = () => {
  const [stats, setStats] = useState({
    totalAdults: 0,
    totalChildren: 0,
    totalGuests: 0,
    totalExpenditure: 0
  });
  const [loading, setLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState(new Date());
  const navigate = useNavigate();

  const fetchStats = async () => {
    setLoading(true);
    try {
      const response = await guestApi.list();
      console.log('Fetched stats:', response.data);
      if (response.data) {
        setStats(response.data);
      }
      setLastUpdated(new Date());
    } catch (err) {
      console.error('Failed to fetch stats:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchStats();
    // Poll every 30 seconds since Google Sheets is not real-time
    const interval = setInterval(fetchStats, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('token');
    navigate('/login');
  };

  const StatCircle = ({ title, value, icon: Icon, color, iconColor }) => (
    <motion.div 
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="bg-white rounded-3xl p-8 flex flex-col items-center justify-center shadow-lg border border-gray-100 min-h-[180px]"
    >
      <div className={`p-4 rounded-2xl mb-4 ${color} ${iconColor}`}>
        <Icon size={32} />
      </div>
      <h3 className="text-gray-500 font-bold uppercase tracking-wider text-[10px] mb-1">{title}</h3>
      <p className="text-4xl font-black text-gray-900">{value ?? 0}</p>
    </motion.div>
  );

  return (
    <div className="min-h-screen bg-slate-50 p-6 md:p-12 text-slate-900">
      <div className="max-w-5xl mx-auto">
        <header className="flex flex-col md:flex-row justify-between items-start md:items-center mb-12 gap-4">
          <div className="flex flex-col">
            <h1 className="text-3xl font-black text-slate-900">Guest Summary</h1>
            <div className="flex items-center gap-2 text-slate-500 text-sm mt-1">
              <RefreshCw size={14} className={loading ? 'animate-spin' : ''} />
              <span>{loading ? 'Refreshing...' : `Last updated: ${lastUpdated.toLocaleTimeString()}`}</span>
            </div>
          </div>
          <button 
            onClick={handleLogout}
            className="px-6 py-2.5 bg-white text-slate-600 font-bold rounded-xl shadow-sm hover:shadow-md hover:text-red-500 transition-all flex items-center gap-2 border border-slate-200"
          >
            <LogOut size={18} /> Logout
          </button>
        </header>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mb-12">
          <StatCircle 
            title="Total Adults" 
            value={stats.totalAdults} 
            icon={Users} 
            color="bg-blue-50" 
            iconColor="text-blue-600"
          />
          <StatCircle 
            title="Total Children" 
            value={stats.totalChildren} 
            icon={Baby} 
            color="bg-rose-50" 
            iconColor="text-rose-600"
          />
          <StatCircle 
            title="Total Guests" 
            value={stats.totalGuests} 
            icon={Calculator} 
            color="bg-amber-50" 
            iconColor="text-amber-600"
          />
          <motion.div 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-indigo-600 rounded-3xl p-8 flex flex-col items-center justify-center shadow-xl lg:col-span-1 text-white min-h-[180px]"
          >
            <div className="p-4 rounded-2xl mb-4 bg-white/20 text-white">
              <DollarSign size={32} />
            </div>
            <h3 className="text-indigo-100 font-bold uppercase tracking-wider text-[10px] mb-1">Total Expenditure</h3>
            <p className="text-4xl font-black">₹{(stats.totalExpenditure || 0).toLocaleString()}</p>
          </motion.div>
        </div>

        {/* Guest List Section */}
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
          className="bg-white rounded-3xl shadow-lg border border-gray-100 overflow-hidden"
        >
          <div className="px-8 py-6 border-b border-gray-100 bg-gray-50/50 flex justify-between items-center">
            <h2 className="text-xl font-bold text-slate-800">Individual Records</h2>
            <span className="text-xs font-bold text-slate-400 uppercase tracking-widest">{stats.guests?.length || 0} Submissions</span>
          </div>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse">
              <thead>
                <tr className="bg-gray-50/50 text-slate-400 text-[10px] uppercase tracking-widest font-black">
                  <th className="px-8 py-4 border-b border-gray-100">Guest Name</th>
                  <th className="px-8 py-4 border-b border-gray-100 text-center">Adults</th>
                  <th className="px-8 py-4 border-b border-gray-100 text-center">Children</th>
                  <th className="px-8 py-4 border-b border-gray-100 text-right">Total</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-50">
                {stats.guests?.length > 0 ? (
                  stats.guests.map((guest, idx) => (
                    <tr key={idx} className="hover:bg-slate-50/80 transition-colors">
                      <td className="px-8 py-4 font-bold text-slate-700">{guest.name}</td>
                      <td className="px-8 py-4 text-center text-blue-600 font-medium">{guest.adults}</td>
                      <td className="px-8 py-4 text-center text-rose-600 font-medium">{guest.children}</td>
                      <td className="px-8 py-4 text-right">
                        <span className="bg-slate-100 text-slate-600 px-3 py-1 rounded-full text-xs font-black">
                          {guest.adults + guest.children}
                        </span>
                      </td>
                    </tr>
                  ))
                ) : (
                  <tr>
                    <td colSpan="4" className="px-8 py-12 text-center text-slate-400 italic">
                      No matching records found in Google Sheets.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </motion.div>

        <div className="mt-12 text-center text-slate-400 text-xs">
          <p>Data refreshed from Google Sheets every 30 seconds.</p>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
