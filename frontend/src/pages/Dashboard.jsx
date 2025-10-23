import React, { useState, useEffect } from 'react';
import api from '../services/api';
import Header from '../components/Headers';
import SearchBar from '../components/SearchBar';
import FamilyList from '../components/FamilyList';
import FamilyForm from '../components/FamilyForm';
import PersonForm from '../components/PersonForm';

const Dashboard = () => {
  // State
  const [families, setFamilies] = useState([]);
  const [filteredFamilies, setFilteredFamilies] = useState([]);
  const [stats, setStats] = useState({ total_families: 0, total_guests: 0 });
  const [searchQuery, setSearchQuery] = useState('');
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Modal states
  const [showFamilyForm, setShowFamilyForm] = useState(false);
  const [showPersonForm, setShowPersonForm] = useState(false);
  const [editingFamily, setEditingFamily] = useState(null);
  const [editingPerson, setEditingPerson] = useState(null);
  const [selectedFamilyId, setSelectedFamilyId] = useState(null);

  // Fetch families on component mount
  useEffect(() => {
    fetchFamilies();
    fetchStats();
  }, []);

  // Filter families when search query changes
  useEffect(() => {
    filterFamilies();
  }, [searchQuery, families]);

  // Fetch all families from API
  const fetchFamilies = async () => {
    try {
      setLoading(true);
      const response = await api.get('/families');
      setFamilies(response.data);
      setError(null);
    } catch (err) {
      console.error('Error fetching families:', err);
      setError('Failed to load families. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch statistics
  const fetchStats = async () => {
    try {
      const response = await api.get('/stats');
      setStats(response.data);
    } catch (err) {
      console.error('Error fetching stats:', err);
    }
  };

  // Filter families based on search query
  const filterFamilies = () => {
    if (!searchQuery.trim()) {
      setFilteredFamilies(families);
      return;
    }

    const query = searchQuery.toLowerCase();
    const filtered = families.filter((family) => {
      // Search in family name
      if (family.family_name.toLowerCase().includes(query)) return true;

      // Search in address
      if (family.address.toLowerCase().includes(query)) return true;

      // Search in member names
      if (family.members && family.members.some((member) =>
        member.name.toLowerCase().includes(query)
      )) return true;

      return false;
    });

    setFilteredFamilies(filtered);
  };

  // Handle search query change
  const handleSearchChange = (query) => {
    setSearchQuery(query);
  };

  // ===== FAMILY OPERATIONS =====

  // Add new family
  const handleAddFamily = async (data) => {
    try {
      await api.post('/families', data);
      await fetchFamilies();
      await fetchStats();
      setShowFamilyForm(false);
      setEditingFamily(null);
    } catch (err) {
      console.error('Error adding family:', err);
      throw err;
    }
  };

  // Update existing family
  const handleUpdateFamily = async (data) => {
    try {
      await api.put(`/families/${data.id}`, data);
      await fetchFamilies();
      setShowFamilyForm(false);
      setEditingFamily(null);
    } catch (err) {
      console.error('Error updating family:', err);
      throw err;
    }
  };

  // Open edit family form
  const handleEditFamily = (family) => {
    setEditingFamily(family);
    setShowFamilyForm(true);
  };

  // Delete family
  const handleDeleteFamily = async (familyId) => {
    try {
      await api.delete(`/families/${familyId}`);
      await fetchFamilies();
      await fetchStats();
    } catch (err) {
      console.error('Error deleting family:', err);
      alert('Failed to delete family. Please try again.');
    }
  };

  // ===== PERSON OPERATIONS =====

  // Add new member
  const handleAddMember = (familyId) => {
    setSelectedFamilyId(familyId);
    setEditingPerson(null);
    setShowPersonForm(true);
  };

  // Add or update person
  const handleSubmitPerson = async (data) => {
    try {
      if (editingPerson) {
        // Update existing person
        await api.put(`/persons/${data.id}`, { name: data.name });
      } else {
        // Add new person
        await api.post('/persons', data);
      }
      await fetchFamilies();
      await fetchStats();
      setShowPersonForm(false);
      setEditingPerson(null);
      setSelectedFamilyId(null);
    } catch (err) {
      console.error('Error saving person:', err);
      throw err;
    }
  };

  // Open edit person form
  const handleEditPerson = (person) => {
    setEditingPerson(person);
    setShowPersonForm(true);
  };

  // Delete person
  const handleDeletePerson = async (personId) => {
    try {
      await api.delete(`/persons/${personId}`);
      await fetchFamilies();
      await fetchStats();
    } catch (err) {
      console.error('Error deleting person:', err);
      alert('Failed to delete member. Please try again.');
    }
  };

  // ===== EXPORT =====

  // Handle export
  const handleExport = async (format) => {
    try {
      const response = await api.get(`/export/${format}`, {
        responseType: 'blob',
      });

      // Create download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      
      const date = new Date().toLocaleDateString('en-GB').replace(/\//g, '_');
      const extension = format === 'excel' ? 'xlsx' : 'csv';
      link.setAttribute('download', `wedding_guests_${date}.${extension}`);
      
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (err) {
      console.error('Error exporting:', err);
      alert('Failed to export. Please try again.');
    }
  };

  // ===== RENDER =====

  if (loading && families.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <svg
            className="animate-spin h-12 w-12 text-blue-600 mx-auto mb-4"
            fill="none"
            viewBox="0 0 24 24"
          >
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <p className="text-gray-600 font-medium">Loading guest list...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <svg
            className="w-16 h-16 text-red-500 mx-auto mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
            />
          </svg>
          <p className="text-red-600 font-medium mb-4">{error}</p>
          <button onClick={fetchFamilies} className="btn-primary">
            Try Again
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <Header
        stats={stats}
        onAddFamily={() => {
          setEditingFamily(null);
          setShowFamilyForm(true);
        }}
        onExport={handleExport}
      />

      {/* Search Bar */}
      <SearchBar searchQuery={searchQuery} onSearchChange={handleSearchChange} />

      {/* Family List */}
      <FamilyList
        families={filteredFamilies}
        onEditFamily={handleEditFamily}
        onDeleteFamily={handleDeleteFamily}
        onAddMember={handleAddMember}
        onEditPerson={handleEditPerson}
        onDeletePerson={handleDeletePerson}
      />

      {/* Family Form Modal */}
      <FamilyForm
        isOpen={showFamilyForm}
        onClose={() => {
          setShowFamilyForm(false);
          setEditingFamily(null);
        }}
        onSubmit={editingFamily ? handleUpdateFamily : handleAddFamily}
        family={editingFamily}
      />

      {/* Person Form Modal */}
      <PersonForm
        isOpen={showPersonForm}
        onClose={() => {
          setShowPersonForm(false);
          setEditingPerson(null);
          setSelectedFamilyId(null);
        }}
        onSubmit={handleSubmitPerson}
        person={editingPerson}
        familyId={selectedFamilyId}
      />
    </div>
  );
};

export default Dashboard;
