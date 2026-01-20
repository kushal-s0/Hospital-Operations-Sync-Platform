import React, { useState, useEffect } from 'react';
import { StatusBadge } from '../../components/Common';
import { bedsAPI } from '../../services/api';
import './BedManagement.css';

const BedManagement = () => {
  const [selectedDepartment, setSelectedDepartment] = useState('all');
  const [selectedStatus, setSelectedStatus] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [beds, setBeds] = useState([]);
  const [departments, setDepartments] = useState([{ id: 'all', name: 'All Departments' }]);
  const [allDepartments, setAllDepartments] = useState([]);
  const [hospitals, setHospitals] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [showModal, setShowModal] = useState(false);
  const [formData, setFormData] = useState({
    bed_id: '',
    hospital: '',
    department: '',
    bed_type: 'Normal',
    status: 'Available'
  });
  const [formError, setFormError] = useState(null);
  const [submitting, setSubmitting] = useState(false);
  const [loadingFormData, setLoadingFormData] = useState(false);
  const [showStatusModal, setShowStatusModal] = useState(false);
  const [statusFormData, setStatusFormData] = useState({
    bed_id: '',
    current_status: '',
    new_status: ''
  });
  const [statusError, setStatusError] = useState(null);
  const [updatingStatus, setUpdatingStatus] = useState(false);
  const [fetchingBedStatus, setFetchingBedStatus] = useState(false);
  const [showDiscardModal, setShowDiscardModal] = useState(false);
  const [discardFormData, setDiscardFormData] = useState({
    bed_id: '',
    bedDetails: null
  });
  const [discardError, setDiscardError] = useState(null);
  const [discarding, setDiscarding] = useState(false);
  const [fetchingBedDetails, setFetchingBedDetails] = useState(false);
  const [showConfirmation, setShowConfirmation] = useState(false);
  const [showUpdateModal, setShowUpdateModal] = useState(false);
  const [updateFormData, setUpdateFormData] = useState({
    bed_id: '',
    hospital: '',
    department: '',
    bed_type: '',
    status: ''
  });
  const [updateError, setUpdateError] = useState(null);
  const [updatingBed, setUpdatingBed] = useState(false);
  const [fetchingUpdateDetails, setFetchingUpdateDetails] = useState(false);

  useEffect(() => {
    const fetchData = async () => {
      try {
        setLoading(true);
        setError(null);
        
        // Fetch beds and occupancy summary first
        const [bedsResponse, occupancyResponse] = await Promise.all([
          bedsAPI.getAll(),
          bedsAPI.getOccupancySummary()
        ]);
        
        // Handle paginated response - data may be in .results or directly in .data
        const responseData = bedsResponse.data;
        const bedsData = Array.isArray(responseData) 
          ? responseData 
          : (responseData.results || []);
        setBeds(bedsData);
        
        // Build departments list from occupancy summary
        const deptList = [{ id: 'all', name: 'All Departments' }];
        const deptData = Array.isArray(occupancyResponse.data) 
          ? occupancyResponse.data 
          : (occupancyResponse.data.results || []);
        // Use Set to avoid duplicates
        const uniqueDepts = new Set();
        deptData.forEach(dept => {
          if (!uniqueDepts.has(dept.department)) {
            uniqueDepts.add(dept.department);
            deptList.push({ id: dept.department, name: dept.department });
          }
        });
        setDepartments(deptList);

        // Fetch hospitals and departments for form (non-critical)
        try {
          const [hospitalsResponse, departmentsResponse] = await Promise.all([
            bedsAPI.getHospitals(),
            bedsAPI.getDepartments()
          ]);

          const hospitalsData = Array.isArray(hospitalsResponse.data) 
            ? hospitalsResponse.data 
            : (hospitalsResponse.data.results || []);
          setHospitals(hospitalsData);

          const allDeptData = Array.isArray(departmentsResponse.data) 
            ? departmentsResponse.data 
            : (departmentsResponse.data.results || []);
          setAllDepartments(allDeptData);
        } catch (formDataErr) {
          console.warn('Failed to fetch form data (hospitals/departments):', formDataErr);
          // This is non-critical, so we don't set error state
        }
      } catch (err) {
        console.error('Failed to fetch beds data:', err);
        setError('Failed to load bed data. Please try again.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const handleOpenModal = async () => {
    setShowModal(true);
    setFormData({
      bed_id: '',
      hospital: '',
      department: '',
      bed_type: 'Normal',
      status: 'Available'
    });
    setFormError(null);

    // Fetch form data if not already loaded
    if (hospitals.length === 0 || allDepartments.length === 0) {
      setLoadingFormData(true);
      try {
        const [hospitalsResponse, departmentsResponse] = await Promise.all([
          bedsAPI.getHospitals(),
          bedsAPI.getDepartments()
        ]);

        const hospitalsData = Array.isArray(hospitalsResponse.data) 
          ? hospitalsResponse.data 
          : (hospitalsResponse.data.results || []);
        console.log('Loaded hospitals:', hospitalsData);
        setHospitals(hospitalsData);

        const allDeptData = Array.isArray(departmentsResponse.data) 
          ? departmentsResponse.data 
          : (departmentsResponse.data.results || []);
        console.log('Loaded departments:', allDeptData);
        setAllDepartments(allDeptData);
      } catch (err) {
        console.error('Failed to fetch form data:', err);
        console.error('Error details:', err.response || err.message);
        setFormError(`Failed to load data: ${err.response?.data?.detail || err.message || 'Please check if backend is running'}`);
      } finally {
        setLoadingFormData(false);
      }
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setFormData({
      bed_id: '',
      hospital: '',
      department: '',
      bed_type: 'Normal',
      status: 'Available'
    });
    setFormError(null);
  };

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setFormError(null);
    setSubmitting(true);

    try {
      // Validate form data
      if (!formData.bed_id || !formData.hospital || !formData.department) {
        setFormError('Please fill in all required fields');
        setSubmitting(false);
        return;
      }

      // Create the bed
      await bedsAPI.create({
        bed_id: parseInt(formData.bed_id),
        hospital: parseInt(formData.hospital),
        department: parseInt(formData.department),
        bed_type: formData.bed_type,
        status: formData.status
      });

      // Close modal
      handleCloseModal();
      
      // Reload the entire page to get fresh data
      window.location.reload();
    } catch (err) {
      console.error('Failed to create bed:', err);
      setFormError(err.response?.data?.detail || err.response?.data?.bed_id?.[0] || 'Failed to create bed. Please try again.');
    } finally {
      setSubmitting(false);
    }
  };

  const getHospitalName = (hospitalId) => {
    const hospital = hospitals.find(h => h.hospital_id === parseInt(hospitalId));
    return hospital ? hospital.hospital_name : '';
  };

  const getDepartmentName = (departmentId) => {
    const department = allDepartments.find(d => d.department_id === parseInt(departmentId));
    return department ? department.department_name : '';
  };

  const handleOpenStatusModal = () => {
    setShowStatusModal(true);
    setStatusFormData({
      bed_id: '',
      current_status: '',
      new_status: ''
    });
    setStatusError(null);
  };

  const handleCloseStatusModal = () => {
    setShowStatusModal(false);
    setStatusFormData({
      bed_id: '',
      current_status: '',
      new_status: ''
    });
    setStatusError(null);
  };

  const handleStatusInputChange = (e) => {
    const { name, value } = e.target;
    setStatusFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFetchBedStatus = async () => {
    if (!statusFormData.bed_id) {
      setStatusError('Please enter a bed ID');
      return;
    }

    setFetchingBedStatus(true);
    setStatusError(null);

    try {
      const bed = bedsArray.find(b => b.bed_id === parseInt(statusFormData.bed_id));
      if (bed) {
        setStatusFormData(prev => ({
          ...prev,
          current_status: bed.status,
          new_status: bed.status,
          bedData: bed  // Store complete bed data for update
        }));
      } else {
        setStatusError(`Bed #${statusFormData.bed_id} not found`);
      }
    } catch (err) {
      setStatusError('Failed to fetch bed status');
    } finally {
      setFetchingBedStatus(false);
    }
  };

  const handleStatusSubmit = async (e) => {
    e.preventDefault();
    setStatusError(null);
    setUpdatingStatus(true);

    try {
      if (!statusFormData.bed_id || !statusFormData.new_status || !statusFormData.bedData) {
        setStatusError('Please fill in all required fields');
        setUpdatingStatus(false);
        return;
      }

      // Update the bed status using PATCH (partial update)
      await bedsAPI.patch(statusFormData.bed_id, {
        status: statusFormData.new_status
      });

      // Close modal and reload page
      handleCloseStatusModal();
      window.location.reload();
    } catch (err) {
      console.error('Failed to update bed status:', err);
      console.error('Error response:', err.response?.data);
      setStatusError(err.response?.data?.detail || err.response?.data?.status?.[0] || 'Failed to update bed status. Please try again.');
    } finally {
      setUpdatingStatus(false);
    }
  };

  const handleOpenDiscardModal = () => {
    setShowDiscardModal(true);
    setDiscardFormData({
      bed_id: '',
      bedDetails: null
    });
    setDiscardError(null);
    setShowConfirmation(false);
  };

  const handleCloseDiscardModal = () => {
    setShowDiscardModal(false);
    setDiscardFormData({
      bed_id: '',
      bedDetails: null
    });
    setDiscardError(null);
    setShowConfirmation(false);
  };

  const handleDiscardInputChange = (e) => {
    const { value } = e.target;
    setDiscardFormData(prev => ({
      ...prev,
      bed_id: value,
      bedDetails: null
    }));
    setShowConfirmation(false);
  };

  const handleFetchBedDetails = async () => {
    if (!discardFormData.bed_id) {
      setDiscardError('Please enter a bed ID');
      return;
    }

    setFetchingBedDetails(true);
    setDiscardError(null);

    try {
      const bed = bedsArray.find(b => b.bed_id === parseInt(discardFormData.bed_id));
      if (bed) {
        setDiscardFormData(prev => ({
          ...prev,
          bedDetails: bed
        }));
      } else {
        setDiscardError(`Bed #${discardFormData.bed_id} not found`);
      }
    } catch (err) {
      setDiscardError('Failed to fetch bed details');
    } finally {
      setFetchingBedDetails(false);
    }
  };

  const handleDiscardClick = () => {
    if (!discardFormData.bedDetails) {
      setDiscardError('Please fetch bed details first');
      return;
    }
    setShowConfirmation(true);
  };

  const handleConfirmDiscard = async () => {
    setDiscardError(null);
    setDiscarding(true);

    try {
      await bedsAPI.delete(discardFormData.bed_id);
      handleCloseDiscardModal();
      window.location.reload();
    } catch (err) {
      console.error('Failed to discard bed:', err);
      setDiscardError(err.response?.data?.detail || 'Failed to discard bed. Please try again.');
      setShowConfirmation(false);
    } finally {
      setDiscarding(false);
    }
  };

  const handleOpenUpdateModal = () => {
    setShowUpdateModal(true);
    setUpdateFormData({
      bed_id: '',
      hospital: '',
      department: '',
      bed_type: '',
      status: ''
    });
    setUpdateError(null);
  };

  const handleCloseUpdateModal = () => {
    setShowUpdateModal(false);
    setUpdateFormData({
      bed_id: '',
      hospital: '',
      department: '',
      bed_type: '',
      status: ''
    });
    setUpdateError(null);
  };

  const handleUpdateInputChange = (e) => {
    const { name, value } = e.target;
    setUpdateFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleFetchUpdateDetails = async () => {
    if (!updateFormData.bed_id) {
      setUpdateError('Please enter a bed ID');
      return;
    }

    setFetchingUpdateDetails(true);
    setUpdateError(null);

    try {
      const bed = bedsArray.find(b => b.bed_id === parseInt(updateFormData.bed_id));
      if (bed) {
        setUpdateFormData({
          bed_id: bed.bed_id,
          hospital: bed.hospital || '',
          department: bed.department || '',
          bed_type: bed.bed_type,
          status: bed.status
        });
      } else {
        setUpdateError(`Bed #${updateFormData.bed_id} not found`);
      }
    } catch (err) {
      setUpdateError('Failed to fetch bed details');
    } finally {
      setFetchingUpdateDetails(false);
    }
  };

  const handleUpdateSubmit = async (e) => {
    e.preventDefault();
    setUpdateError(null);
    setUpdatingBed(true);

    try {
      if (!updateFormData.bed_id || !updateFormData.hospital || !updateFormData.department) {
        setUpdateError('Please fill in all required fields');
        setUpdatingBed(false);
        return;
      }

      // Update the bed with all fields using PATCH
      await bedsAPI.patch(updateFormData.bed_id, {
        hospital: parseInt(updateFormData.hospital),
        department: parseInt(updateFormData.department),
        bed_type: updateFormData.bed_type,
        status: updateFormData.status
      });

      handleCloseUpdateModal();
      window.location.reload();
    } catch (err) {
      console.error('Failed to update bed:', err);
      console.error('Error details:', err.response?.data);
      setUpdateError(
        err.response?.data?.detail || 
        err.response?.data?.hospital?.[0] || 
        err.response?.data?.department?.[0] ||
        'Failed to update bed. Please try again.'
      );
    } finally {
      setUpdatingBed(false);
    }
  };

  // Ensure beds is always an array
  const bedsArray = Array.isArray(beds) ? beds : [];
  
  const filteredBeds = bedsArray.filter(bed => {
    const matchesDepartment = selectedDepartment === 'all' || bed.department_name === selectedDepartment;
    const matchesStatus = selectedStatus === 'all' || bed.status === selectedStatus;
    
    // Search filter - search in bed_id, department_name, bed_type, and status
    const matchesSearch = searchQuery === '' || 
      bed.bed_id.toString().includes(searchQuery) ||
      bed.department_name?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      bed.bed_type?.toLowerCase().includes(searchQuery.toLowerCase()) ||
      bed.status?.toLowerCase().includes(searchQuery.toLowerCase());
    
    return matchesDepartment && matchesStatus && matchesSearch;
  });

  const stats = {
    total: bedsArray.length,
    available: bedsArray.filter(b => b.status === 'Available').length,
    occupied: bedsArray.filter(b => b.status === 'Occupied').length,
    maintenance: bedsArray.filter(b => b.status === 'Maintenance').length,
  };

  return (
    <div className="bed-management">
      <div className="page-header">
        <div>
          <h1>Live Bed Availability Dashboard</h1>
          <p>Real-time bed occupancy and availability status</p>
        </div>
        <div className="header-actions">
          <button className="update-status-btn" onClick={handleOpenStatusModal}>
            Update Bed Status
          </button>
          <button className="update-details-btn" onClick={handleOpenUpdateModal}>
            Update Bed Details
          </button>
          <button className="discard-bed-btn" onClick={handleOpenDiscardModal}>
            Discard Bed
          </button>
          <button className="add-bed-btn" onClick={handleOpenModal}>
            + Add New Bed
          </button>
        </div>
      </div>

      {loading && <div className="loading">Loading bed data...</div>}
      {error && <div className="error-message">{error}</div>}

      {!loading && !error && (
        <>
          <div className="bed-stats">
            <div className="stat-card total">
              <span className="stat-value">{stats.total}</span>
              <span className="stat-label">Total Beds</span>
            </div>
            <div className="stat-card available">
              <span className="stat-value">{stats.available}</span>
              <span className="stat-label">Available</span>
            </div>
            <div className="stat-card occupied">
              <span className="stat-value">{stats.occupied}</span>
              <span className="stat-label">Occupied</span>
            </div>
            <div className="stat-card maintenance">
              <span className="stat-value">{stats.maintenance}</span>
              <span className="stat-label">Maintenance</span>
            </div>
          </div>

          <div className="search-section">
            <input
              type="text"
              className="search-input"
              placeholder="Search beds by ID, department, type, or status..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
            {searchQuery && (
              <button className="clear-search" onClick={() => setSearchQuery('')}>
                &times;
              </button>
            )}
          </div>

          <div className="filter-section">
            <div className="filter-group">
              <label>Filter by Department:</label>
              <select 
                value={selectedDepartment} 
                onChange={(e) => setSelectedDepartment(e.target.value)}
              >
                {departments.map(dept => (
                  <option key={dept.id} value={dept.id}>{dept.name}</option>
                ))}
              </select>
            </div>
            <div className="filter-group">
              <label>Filter by Status:</label>
              <select 
                value={selectedStatus} 
                onChange={(e) => setSelectedStatus(e.target.value)}
              >
                <option value="all">All Statuses</option>
                <option value="Available">Available</option>
                <option value="Occupied">Occupied</option>
                <option value="Maintenance">Maintenance</option>
              </select>
            </div>
          </div>

          <div className="beds-grid">
            {filteredBeds.length === 0 ? (
              <p className="no-data">No beds found</p>
            ) : (
              filteredBeds.map(bed => (
                <div key={bed.bed_id} className={`bed-card bed-${bed.status.toLowerCase()}`}>
                  <div className="bed-header">
                    <span className="bed-number">Bed #{bed.bed_id}</span>
                    <StatusBadge status={bed.status.toLowerCase()} />
                  </div>
                  <div className="bed-info">
                    <p><strong>Department:</strong> {bed.department_name}</p>
                    <p><strong>Type:</strong> {bed.bed_type}</p>
                  </div>
                </div>
              ))
            )}
          </div>
        </>
      )}

      {/* Add Bed Modal */}
      {showModal && (
        <div className="modal-overlay" onClick={handleCloseModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Add New Bed</h2>
              <button className="close-btn" onClick={handleCloseModal}>&times;</button>
            </div>
            
            {formError && <div className="form-error">{formError}</div>}
            
            {loadingFormData ? (
              <div className="loading-form-data">Loading hospitals and departments...</div>
            ) : (
              <form onSubmit={handleSubmit} className="bed-form">
                <div className="form-group">
                  <label htmlFor="bed_id">Bed ID <span className="required">*</span></label>
                  <input
                    type="number"
                    id="bed_id"
                    name="bed_id"
                    value={formData.bed_id}
                    onChange={handleInputChange}
                    required
                    placeholder="Enter bed ID"
                  />
                </div>

                <div className="form-group">
                  <label htmlFor="hospital">Hospital <span className="required">*</span></label>
                  <select
                    id="hospital"
                    name="hospital"
                    value={formData.hospital}
                    onChange={handleInputChange}
                    required
                    disabled={loadingFormData}
                  >
                    <option value="">Select Hospital</option>
                    {hospitals.map(hospital => (
                      <option key={hospital.hospital_id} value={hospital.hospital_id}>
                        {hospital.hospital_name}
                      </option>
                    ))}
                  </select>
                  {hospitals.length === 0 && !loadingFormData && (
                    <span className="field-warning">No hospitals available</span>
                  )}
                  {formData.hospital && (
                    <span className="field-info">Selected: {getHospitalName(formData.hospital)}</span>
                  )}
                </div>

                <div className="form-group">
                  <label htmlFor="department">Department <span className="required">*</span></label>
                  <select
                    id="department"
                    name="department"
                    value={formData.department}
                    onChange={handleInputChange}
                    required
                    disabled={loadingFormData}
                  >
                    <option value="">Select Department</option>
                    {allDepartments.map(dept => (
                      <option key={dept.department_id} value={dept.department_id}>
                        {dept.department_name}
                      </option>
                    ))}
                  </select>
                  {allDepartments.length === 0 && !loadingFormData && (
                    <span className="field-warning">No departments available</span>
                  )}
                  {formData.department && (
                    <span className="field-info">Selected: {getDepartmentName(formData.department)}</span>
                  )}
                </div>

                <div className="form-group">
                  <label htmlFor="bed_type">Bed Type <span className="required">*</span></label>
                  <select
                    id="bed_type"
                    name="bed_type"
                    value={formData.bed_type}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="Normal">Normal</option>
                    <option value="ICU">ICU</option>
                    <option value="Ventilator">Ventilator</option>
                    <option value="Emergency">Emergency</option>
                  </select>
                </div>

                <div className="form-group">
                  <label htmlFor="status">Status <span className="required">*</span></label>
                  <select
                    id="status"
                    name="status"
                    value={formData.status}
                    onChange={handleInputChange}
                    required
                  >
                    <option value="Available">Available</option>
                    <option value="Occupied">Occupied</option>
                    <option value="Maintenance">Maintenance</option>
                  </select>
                </div>

                <div className="form-actions">
                  <button type="button" className="cancel-btn" onClick={handleCloseModal}>
                    Cancel
                  </button>
                  <button type="submit" className="submit-btn" disabled={submitting}>
                    {submitting ? 'Adding...' : 'Add Bed'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}

      {/* Update Bed Status Modal */}
      {showStatusModal && (
        <div className="modal-overlay" onClick={handleCloseStatusModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Update Bed Status</h2>
              <button className="close-btn" onClick={handleCloseStatusModal}>&times;</button>
            </div>
            
            {statusError && <div className="form-error">{statusError}</div>}
            
            <form onSubmit={handleStatusSubmit} className="bed-form">
              <div className="form-group">
                <label htmlFor="status_bed_id">Bed ID <span className="required">*</span></label>
                <div className="bed-id-input-group">
                  <input
                    type="number"
                    id="status_bed_id"
                    name="bed_id"
                    value={statusFormData.bed_id}
                    onChange={handleStatusInputChange}
                    required
                    placeholder="Enter bed ID"
                  />
                  <button 
                    type="button" 
                    className="fetch-status-btn"
                    onClick={handleFetchBedStatus}
                    disabled={fetchingBedStatus}
                  >
                    {fetchingBedStatus ? 'Loading...' : 'Get Status'}
                  </button>
                </div>
              </div>

              {statusFormData.current_status && (
                <>
                  <div className="form-group">
                    <label>Current Status</label>
                    <div className="current-status-display">
                      <span className={`status-badge status-${statusFormData.current_status.toLowerCase()}`}>
                        {statusFormData.current_status}
                      </span>
                    </div>
                  </div>

                  <div className="form-group">
                    <label htmlFor="new_status">New Status <span className="required">*</span></label>
                    <select
                      id="new_status"
                      name="new_status"
                      value={statusFormData.new_status}
                      onChange={handleStatusInputChange}
                      required
                    >
                      <option value="Available">Available</option>
                      <option value="Occupied">Occupied</option>
                      <option value="Maintenance">Maintenance</option>
                    </select>
                  </div>
                </>
              )}

              <div className="form-actions">
                <button type="button" className="cancel-btn" onClick={handleCloseStatusModal}>
                  Cancel
                </button>
                <button 
                  type="submit" 
                  className="submit-btn" 
                  disabled={updatingStatus || !statusFormData.current_status}
                >
                  {updatingStatus ? 'Updating...' : 'Update Status'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Discard Bed Modal */}
      {showDiscardModal && (
        <div className="modal-overlay" onClick={handleCloseDiscardModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Discard Bed</h2>
              <button className="close-btn" onClick={handleCloseDiscardModal}>&times;</button>
            </div>
            
            {discardError && <div className="form-error">{discardError}</div>}
            
            {!showConfirmation ? (
              <div className="bed-form">
                <div className="form-group">
                  <label htmlFor="discard_bed_id">Bed ID <span className="required">*</span></label>
                  <div className="bed-id-input-group">
                    <input
                      type="number"
                      id="discard_bed_id"
                      name="bed_id"
                      value={discardFormData.bed_id}
                      onChange={handleDiscardInputChange}
                      required
                      placeholder="Enter bed ID"
                    />
                    <button 
                      type="button" 
                      className="fetch-status-btn"
                      onClick={handleFetchBedDetails}
                      disabled={fetchingBedDetails}
                    >
                      {fetchingBedDetails ? 'Loading...' : 'Get Details'}
                    </button>
                  </div>
                </div>

                {discardFormData.bedDetails && (
                  <div className="bed-details-display">
                    <h3>Bed Details</h3>
                    <div className="detail-row">
                      <span className="detail-label">Bed ID:</span>
                      <span className="detail-value">#{discardFormData.bedDetails.bed_id}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Department:</span>
                      <span className="detail-value">{discardFormData.bedDetails.department_name}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Bed Type:</span>
                      <span className="detail-value">{discardFormData.bedDetails.bed_type}</span>
                    </div>
                    <div className="detail-row">
                      <span className="detail-label">Status:</span>
                      <span className={`status-badge status-${discardFormData.bedDetails.status.toLowerCase()}`}>
                        {discardFormData.bedDetails.status}
                      </span>
                    </div>
                  </div>
                )}

                <div className="form-actions">
                  <button type="button" className="cancel-btn" onClick={handleCloseDiscardModal}>
                    Cancel
                  </button>
                  <button 
                    type="button" 
                    className="discard-btn" 
                    onClick={handleDiscardClick}
                    disabled={!discardFormData.bedDetails}
                  >
                    Discard Bed
                  </button>
                </div>
              </div>
            ) : (
              <div className="confirmation-dialog">
                <div className="confirmation-icon">⚠️</div>
                <h3>Confirm Bed Discard</h3>
                <p>Are you sure you want to discard Bed #{discardFormData.bed_id}?</p>
                <p className="warning-text">This action cannot be undone.</p>
                
                <div className="bed-details-summary">
                  <strong>Bed Details:</strong>
                  <ul>
                    <li>Department: {discardFormData.bedDetails.department_name}</li>
                    <li>Type: {discardFormData.bedDetails.bed_type}</li>
                    <li>Status: {discardFormData.bedDetails.status}</li>
                  </ul>
                </div>

                <div className="form-actions">
                  <button 
                    type="button" 
                    className="cancel-btn" 
                    onClick={() => setShowConfirmation(false)}
                    disabled={discarding}
                  >
                    Cancel
                  </button>
                  <button 
                    type="button" 
                    className="confirm-discard-btn" 
                    onClick={handleConfirmDiscard}
                    disabled={discarding}
                  >
                    {discarding ? 'Discarding...' : 'Yes, Discard Bed'}
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Update Bed Details Modal */}
      {showUpdateModal && (
        <div className="modal-overlay" onClick={handleCloseUpdateModal}>
          <div className="modal-content" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>Update Bed Details</h2>
              <button className="close-btn" onClick={handleCloseUpdateModal}>&times;</button>
            </div>
            
            {updateError && <div className="form-error">{updateError}</div>}
            
            {loadingFormData ? (
              <div className="loading-form-data">Loading hospitals and departments...</div>
            ) : (
              <form onSubmit={handleUpdateSubmit} className="bed-form">
                <div className="form-group">
                  <label htmlFor="update_bed_id">Bed ID <span className="required">*</span></label>
                  <div className="bed-id-input-group">
                    <input
                      type="number"
                      id="update_bed_id"
                      name="bed_id"
                      value={updateFormData.bed_id}
                      onChange={handleUpdateInputChange}
                      required
                      placeholder="Enter bed ID"
                      disabled={updateFormData.hospital !== ''}
                    />
                    {!updateFormData.hospital && (
                      <button 
                        type="button" 
                        className="fetch-status-btn"
                        onClick={handleFetchUpdateDetails}
                        disabled={fetchingUpdateDetails}
                      >
                        {fetchingUpdateDetails ? 'Loading...' : 'Get Details'}
                      </button>
                    )}
                  </div>
                </div>

                {updateFormData.hospital && (
                  <>
                    <div className="form-group">
                      <label htmlFor="update_hospital">Hospital <span className="required">*</span></label>
                      <select
                        id="update_hospital"
                        name="hospital"
                        value={updateFormData.hospital}
                        onChange={handleUpdateInputChange}
                        required
                      >
                        <option value="">Select Hospital</option>
                        {hospitals.map(hospital => (
                          <option key={hospital.hospital_id} value={hospital.hospital_id}>
                            {hospital.hospital_name}
                          </option>
                        ))}
                      </select>
                      {updateFormData.hospital && (
                        <span className="field-info">Selected: {getHospitalName(updateFormData.hospital)}</span>
                      )}
                    </div>

                    <div className="form-group">
                      <label htmlFor="update_department">Department <span className="required">*</span></label>
                      <select
                        id="update_department"
                        name="department"
                        value={updateFormData.department}
                        onChange={handleUpdateInputChange}
                        required
                      >
                        <option value="">Select Department</option>
                        {allDepartments.map(dept => (
                          <option key={dept.department_id} value={dept.department_id}>
                            {dept.department_name}
                          </option>
                        ))}
                      </select>
                      {updateFormData.department && (
                        <span className="field-info">Selected: {getDepartmentName(updateFormData.department)}</span>
                      )}
                    </div>

                    <div className="form-group">
                      <label htmlFor="update_bed_type">Bed Type <span className="required">*</span></label>
                      <select
                        id="update_bed_type"
                        name="bed_type"
                        value={updateFormData.bed_type}
                        onChange={handleUpdateInputChange}
                        required
                      >
                        <option value="Normal">Normal</option>
                        <option value="ICU">ICU</option>
                        <option value="Ventilator">Ventilator</option>
                        <option value="Emergency">Emergency</option>
                      </select>
                    </div>

                    <div className="form-group">
                      <label htmlFor="update_status">Status <span className="required">*</span></label>
                      <select
                        id="update_status"
                        name="status"
                        value={updateFormData.status}
                        onChange={handleUpdateInputChange}
                        required
                      >
                        <option value="Available">Available</option>
                        <option value="Occupied">Occupied</option>
                        <option value="Maintenance">Maintenance</option>
                      </select>
                    </div>
                  </>
                )}

                <div className="form-actions">
                  <button type="button" className="cancel-btn" onClick={handleCloseUpdateModal}>
                    Cancel
                  </button>
                  <button 
                    type="submit" 
                    className="submit-btn" 
                    disabled={updatingBed || !updateFormData.hospital}
                  >
                    {updatingBed ? 'Updating...' : 'Update Bed'}
                  </button>
                </div>
              </form>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default BedManagement;
