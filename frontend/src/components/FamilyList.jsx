import React from 'react';
import FamilyCard from './FamilyCard';

const FamilyList = ({ 
  families, 
  onEditFamily, 
  onDeleteFamily, 
  onAddMember, 
  onEditPerson, 
  onDeletePerson 
}) => {
  // Empty state - no families
  if (!families || families.length === 0) {
    return (
      <div className="flex flex-col items-center justify-center py-16 px-4">
        <div className="text-center">
          <svg
            className="w-24 h-24 mx-auto text-gray-300 mb-4"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"
            />
          </svg>
          <h3 className="text-xl font-semibold text-gray-700 mb-2">
            No Families Yet
          </h3>
          <p className="text-gray-500 mb-6">
            Get started by adding your first family to the guest list
          </p>
          <div className="inline-flex items-center gap-2 text-blue-600 font-medium">
            <svg
              className="w-5 h-5"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M12 4v16m8-8H4"
              />
            </svg>
            Click "Add Family" button above to start
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-4 py-6">
      {/* Results Count */}
      <div className="mb-4">
        <p className="text-gray-600">
          Showing <span className="font-semibold text-gray-800">{families.length}</span> 
          {families.length === 1 ? ' family' : ' families'}
        </p>
      </div>

      {/* Family Cards Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {families.map((family) => (
          <FamilyCard
            key={family.id}
            family={family}
            onEdit={onEditFamily}
            onDelete={onDeleteFamily}
            onAddMember={onAddMember}
            onEditPerson={onEditPerson}
            onDeletePerson={onDeletePerson}
          />
        ))}
      </div>
    </div>
  );
};

export default FamilyList;
