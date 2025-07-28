// Reports Dashboard JavaScript
let selectedCases = new Set();
let allCases = [];
let filteredCases = [];
let charts = {};

function initializeReportsDashboard() {
    console.log('Initializing Reports Dashboard...');
    
    // Initialize data
    loadCasesData();
    
    // Initialize charts
    initializeReportsCharts();
    
    // Initialize animated counters
    initializeAnimatedCounters();
    
    // Initialize DataTable if available
    if (typeof $ !== 'undefined' && $.fn.DataTable) {
        initializeDataTable();
    }
    
    // Set up event listeners
    setupReportsEventListeners();
}

function loadCasesData() {
    // Get session ID from URL
    const sessionId = extractSessionIdFromUrl();
    if (!sessionId) {
        console.error('No session ID found');
        return;
    }
    
    // Load cases data from API
    fetch(`/api/cases/${sessionId}`)
        .then(response => response.json())
        .then(data => {
            allCases = data.cases || [];
            filteredCases = [...allCases];
            updateChartsWithData(data);
        })
        .catch(error => {
            console.error('Error loading cases data:', error);
        });
}

function initializeReportsCharts() {
    // Status Distribution Chart
    createStatusDistributionChart();
    
    // Risk Level Chart
    createRiskLevelChart();
    
    // Cases Timeline Chart
    createCasesTimelineChart();
    
    // Top Domains Chart
    createTopDomainsChart();
}

function createStatusDistributionChart() {
    const ctx = document.getElementById('statusDistributionChart');
    if (!ctx) return;
    
    charts.statusDistribution = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Active', 'Cleared', 'Escalated'],
            datasets: [{
                data: [0, 0, 0], // Will be updated with real data
                backgroundColor: [
                    '#17a2b8', // info blue
                    '#28a745', // success green
                    '#dc3545'  // danger red
                ],
                borderWidth: 2,
                borderColor: '#fff'
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom',
                    labels: {
                        padding: 20,
                        usePointStyle: true
                    }
                }
            }
        }
    });
}

function createRiskLevelChart() {
    const ctx = document.getElementById('riskLevelChart');
    if (!ctx) return;
    
    charts.riskLevel = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: ['High Risk', 'Medium Risk', 'Low Risk'],
            datasets: [{
                label: 'Number of Cases',
                data: [0, 0, 0], // Will be updated with real data
                backgroundColor: [
                    '#dc3545', // danger
                    '#ffc107', // warning
                    '#28a745'  // success
                ],
                borderColor: [
                    '#dc3545',
                    '#ffc107',
                    '#28a745'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function createCasesTimelineChart() {
    const ctx = document.getElementById('casesTimelineChart');
    if (!ctx) return;
    
    charts.timeline = new Chart(ctx, {
        type: 'line',
        data: {
            labels: [], // Will be populated with dates
            datasets: [{
                label: 'Cases per Day',
                data: [],
                borderColor: '#007bff',
                backgroundColor: 'rgba(0, 123, 255, 0.1)',
                fill: true,
                tension: 0.4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function createTopDomainsChart() {
    const ctx = document.getElementById('topDomainsChart');
    if (!ctx) return;
    
    charts.topDomains = new Chart(ctx, {
        type: 'horizontalBar',
        data: {
            labels: [],
            datasets: [{
                label: 'Cases',
                data: [],
                backgroundColor: [
                    '#007bff', '#28a745', '#ffc107', '#dc3545', '#6c757d',
                    '#17a2b8', '#fd7e14', '#6f42c1', '#e83e8c', '#20c997'
                ],
                borderWidth: 1
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    display: false
                }
            },
            scales: {
                x: {
                    beginAtZero: true,
                    ticks: {
                        stepSize: 1
                    }
                }
            }
        }
    });
}

function updateChartsWithData(data) {
    // Update status distribution
    if (charts.statusDistribution && data.status_distribution) {
        const statusData = [
            data.status_distribution.Active || 0,
            data.status_distribution.Cleared || 0,
            data.status_distribution.Escalated || 0
        ];
        charts.statusDistribution.data.datasets[0].data = statusData;
        charts.statusDistribution.update();
    }
    
    // Update risk level chart
    if (charts.riskLevel && data.risk_distribution) {
        const riskData = [
            data.risk_distribution.High || 0,
            data.risk_distribution.Medium || 0,
            data.risk_distribution.Low || 0
        ];
        charts.riskLevel.data.datasets[0].data = riskData;
        charts.riskLevel.update();
    }
    
    // Update timeline chart
    if (charts.timeline && data.timeline_data) {
        charts.timeline.data.labels = data.timeline_data.labels || [];
        charts.timeline.data.datasets[0].data = data.timeline_data.data || [];
        charts.timeline.update();
    }
    
    // Update top domains chart
    if (charts.topDomains && data.top_domains) {
        charts.topDomains.data.labels = data.top_domains.labels || [];
        charts.topDomains.data.datasets[0].data = data.top_domains.data || [];
        charts.topDomains.update();
    }
}

function setupReportsEventListeners() {
    // Case selection event listeners are handled by existing main.js
    console.log('Reports event listeners set up');
}

// Case Selection Functions
function toggleSelectAll() {
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    const caseCheckboxes = document.querySelectorAll('.case-checkbox');
    
    caseCheckboxes.forEach(checkbox => {
        checkbox.checked = selectAllCheckbox.checked;
        if (selectAllCheckbox.checked) {
            selectedCases.add(checkbox.value);
        } else {
            selectedCases.delete(checkbox.value);
        }
    });
    
    updateSelection();
}

function selectAllCases() {
    const caseCheckboxes = document.querySelectorAll('.case-checkbox');
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    
    caseCheckboxes.forEach(checkbox => {
        checkbox.checked = true;
        selectedCases.add(checkbox.value);
    });
    
    selectAllCheckbox.checked = true;
    updateSelection();
}

function clearSelection() {
    const caseCheckboxes = document.querySelectorAll('.case-checkbox');
    const selectAllCheckbox = document.getElementById('selectAllCheckbox');
    
    caseCheckboxes.forEach(checkbox => {
        checkbox.checked = false;
    });
    
    selectAllCheckbox.checked = false;
    selectedCases.clear();
    updateSelection();
}

function updateSelection() {
    const selectedCount = selectedCases.size;
    const selectionSummary = document.getElementById('selectionSummary');
    const selectedCountSpan = document.getElementById('selectedCount');
    const selectedSummarySpan = document.getElementById('selectedSummary');
    const bulkUpdateBtn = document.getElementById('bulkUpdateBtn');
    
    selectedCountSpan.textContent = selectedCount;
    
    if (selectedCount > 0) {
        selectionSummary.style.display = 'block';
        bulkUpdateBtn.style.display = 'inline-block';
        
        // Calculate selection summary
        let highRisk = 0, mediumRisk = 0, lowRisk = 0;
        let active = 0, cleared = 0, escalated = 0;
        
        selectedCases.forEach(caseId => {
            const row = document.querySelector(`tr[data-case-id="${caseId}"]`);
            if (row) {
                const risk = row.dataset.risk;
                const status = row.dataset.status;
                
                if (risk === 'High') highRisk++;
                else if (risk === 'Medium') mediumRisk++;
                else lowRisk++;
                
                if (status === 'Active') active++;
                else if (status === 'Cleared') cleared++;
                else escalated++;
            }
        });
        
        selectedSummarySpan.innerHTML = `
            - Risk: ${highRisk} High, ${mediumRisk} Medium, ${lowRisk} Low
            - Status: ${active} Active, ${cleared} Cleared, ${escalated} Escalated
        `;
    } else {
        selectionSummary.style.display = 'none';
        bulkUpdateBtn.style.display = 'none';
    }
}

// Filter Functions
function applyFilters() {
    const statusFilter = document.getElementById('statusFilter').value;
    const riskFilter = document.getElementById('riskFilter').value;
    const dateFilter = document.getElementById('dateFilter').value;
    const searchFilter = document.getElementById('searchFilter').value.toLowerCase();
    
    const rows = document.querySelectorAll('#casesReportTable tbody tr');
    
    rows.forEach(row => {
        let show = true;
        
        // Status filter
        if (statusFilter && row.dataset.status !== statusFilter) {
            show = false;
        }
        
        // Risk filter
        if (riskFilter && row.dataset.risk !== riskFilter) {
            show = false;
        }
        
        // Date filter
        if (dateFilter) {
            const dateCell = row.querySelector('td:nth-child(8)');
            if (dateCell) {
                const rowDate = dateCell.textContent.trim().split(' ')[0];
                if (rowDate !== dateFilter) {
                    show = false;
                }
            }
        }
        
        // Search filter
        if (searchFilter) {
            const text = row.textContent.toLowerCase();
            if (!text.includes(searchFilter)) {
                show = false;
            }
        }
        
        row.style.display = show ? '' : 'none';
    });
}

// Export and Report Functions
function exportSelectedCases() {
    if (selectedCases.size === 0) {
        alert('Please select cases to export');
        return;
    }
    
    const sessionId = extractSessionIdFromUrl();
    const caseIds = Array.from(selectedCases);
    
    // Create form and submit
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/api/export-cases/${sessionId}`;
    
    const input = document.createElement('input');
    input.type = 'hidden';
    input.name = 'case_ids';
    input.value = JSON.stringify(caseIds);
    
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
    document.body.removeChild(form);
}

function generateFullReport() {
    const sessionId = extractSessionIdFromUrl();
    
    // Show loading state
    const btn = event.target;
    const originalText = btn.innerHTML;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Generating...';
    btn.disabled = true;
    
    fetch(`/api/generate-report/${sessionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.blob())
    .then(blob => {
        // Create download link
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `email-security-report-${sessionId}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
    })
    .catch(error => {
        console.error('Error generating report:', error);
        alert('Error generating report. Please try again.');
    })
    .finally(() => {
        btn.innerHTML = originalText;
        btn.disabled = false;
    });
}

function bulkUpdateStatus() {
    if (selectedCases.size === 0) {
        alert('Please select cases to update');
        return;
    }
    
    const newStatus = prompt('Enter new status (Active, Cleared, Escalated):');
    if (!newStatus || !['Active', 'Cleared', 'Escalated'].includes(newStatus)) {
        alert('Invalid status');
        return;
    }
    
    const sessionId = extractSessionIdFromUrl();
    const caseIds = Array.from(selectedCases);
    
    fetch(`/api/bulk-update-status/${sessionId}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            case_ids: caseIds,
            new_status: newStatus
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            location.reload(); // Reload to show updated data
        } else {
            alert('Error updating cases: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Error updating cases:', error);
        alert('Error updating cases. Please try again.');
    });
}

// Initialize DataTable
function initializeDataTable() {
    $('#casesReportTable').DataTable({
        pageLength: 25,
        order: [[7, 'desc']], // Sort by date column
        columnDefs: [
            { orderable: false, targets: [0, 9] }, // Disable sorting for checkbox and actions
            { searchable: false, targets: [0, 9] }
        ],
        dom: 'rt<"d-flex justify-content-between"lp>',
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search cases...",
            lengthMenu: "_MENU_ cases per page"
        }
    });
}

// Utility function to extract session ID from URL
function extractSessionIdFromUrl() {
    const path = window.location.pathname;
    const matches = path.match(/\/reports\/([^/]+)/);
    return matches ? matches[1] : null;
}