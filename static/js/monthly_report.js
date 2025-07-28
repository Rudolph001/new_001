
/**
 * Monthly Report Dashboard JavaScript
 * Handles session selection, report generation, and visualizations
 */

// Global variables
let availableSessions = [];
let selectedSessionIds = new Set();
let reportData = {};
let charts = {};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    loadAvailableSessions();
    initializeEventListeners();
});

// Load available sessions from server
function loadAvailableSessions() {
    fetch('/api/monthly-report/sessions')
        .then(response => response.json())
        .then(data => {
            availableSessions = data.sessions || [];
            renderAvailableSessions();
        })
        .catch(error => {
            console.error('Error loading sessions:', error);
            showNotification('Error loading available sessions', 'error');
        });
}

// Render available sessions list
function renderAvailableSessions() {
    const container = document.getElementById('availableSessions');
    container.innerHTML = '';

    if (availableSessions.length === 0) {
        container.innerHTML = '<p class="text-muted">No sessions available</p>';
        return;
    }

    availableSessions.forEach(session => {
        const sessionElement = document.createElement('div');
        sessionElement.className = 'session-item';
        sessionElement.dataset.sessionId = session.id;
        sessionElement.innerHTML = `
            <div class="d-flex justify-content-between align-items-center">
                <div>
                    <strong>${session.filename}</strong>
                    <br>
                    <small class="text-muted">
                        ${new Date(session.upload_time).toLocaleDateString()} | 
                        ${session.total_records} records
                    </small>
                </div>
                <div class="text-end">
                    <small class="badge bg-${getStatusBadgeColor(session.status)}">${session.status}</small>
                </div>
            </div>
        `;
        
        sessionElement.addEventListener('click', () => toggleSessionSelection(session.id));
        container.appendChild(sessionElement);
    });
}

// Toggle session selection
function toggleSessionSelection(sessionId) {
    const sessionElement = document.querySelector(`[data-session-id="${sessionId}"]`);
    
    if (selectedSessionIds.has(sessionId)) {
        selectedSessionIds.delete(sessionId);
        sessionElement.classList.remove('selected');
    } else {
        selectedSessionIds.add(sessionId);
        sessionElement.classList.add('selected');
    }
    
    updateSelectedSessions();
}

// Update selected sessions display
function updateSelectedSessions() {
    const container = document.getElementById('selectedSessions');
    const infoElement = document.getElementById('selectionInfo');
    
    container.innerHTML = '';
    
    if (selectedSessionIds.size === 0) {
        container.innerHTML = '<p class="text-muted">No sessions selected</p>';
        infoElement.textContent = 'No sessions selected';
        document.getElementById('reportControls').style.display = 'none';
        hideReportSections();
        return;
    }

    selectedSessionIds.forEach(sessionId => {
        const session = availableSessions.find(s => s.id === sessionId);
        if (session) {
            const sessionElement = document.createElement('div');
            sessionElement.className = 'session-item selected';
            sessionElement.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <strong>${session.filename}</strong>
                        <br>
                        <small>${new Date(session.upload_time).toLocaleDateString()}</small>
                    </div>
                    <button class="btn btn-sm btn-outline-light" onclick="removeFromSelection('${sessionId}')">
                        <i class="fas fa-times"></i>
                    </button>
                </div>
            `;
            container.appendChild(sessionElement);
        }
    });
    
    infoElement.textContent = `${selectedSessionIds.size} session(s) selected`;
    document.getElementById('reportControls').style.display = 'block';
}

// Remove session from selection
function removeFromSelection(sessionId) {
    selectedSessionIds.delete(sessionId);
    document.querySelector(`[data-session-id="${sessionId}"]`).classList.remove('selected');
    updateSelectedSessions();
}

// Clear all selections
function clearSelection() {
    selectedSessionIds.clear();
    document.querySelectorAll('.session-item').forEach(el => el.classList.remove('selected'));
    updateSelectedSessions();
}

// Initialize event listeners
function initializeEventListeners() {
    // Report period change
    document.getElementById('reportPeriod').addEventListener('change', function() {
        const customRange = document.getElementById('customDateRange');
        customRange.style.display = this.value === 'custom' ? 'block' : 'none';
    });
}

// Generate report
function generateReport() {
    if (selectedSessionIds.size === 0) {
        showNotification('Please select at least one session', 'warning');
        return;
    }

    showLoading('Generating monthly report...');
    
    const reportConfig = {
        session_ids: Array.from(selectedSessionIds),
        period: document.getElementById('reportPeriod').value,
        format: document.getElementById('reportFormat').value,
        start_date: document.getElementById('startDate').value,
        end_date: document.getElementById('endDate').value
    };

    fetch('/api/monthly-report/generate', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(reportConfig)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            throw new Error(data.error);
        }
        
        reportData = data;
        renderReport();
        hideLoading();
        showNotification('Report generated successfully', 'success');
    })
    .catch(error => {
        console.error('Error generating report:', error);
        hideLoading();
        showNotification('Error generating report: ' + error.message, 'error');
    });
}

// Update report with new parameters
function updateReport() {
    generateReport();
}

// Render the complete report
function renderReport() {
    updateSummaryCards();
    createCharts();
    renderTopRisksTable();
    renderRecommendations();
    showReportSections();
}

// Update summary cards with data
function updateSummaryCards() {
    const summary = reportData.summary || {};
    
    // Animate counters
    animateCounter('totalEmailsProcessed', summary.total_emails || 0);
    animateCounter('securityIncidents', summary.security_incidents || 0);
    animateCounter('casesResolved', summary.cases_resolved || 0);
    
    // Update other metrics
    document.getElementById('avgResponseTime').textContent = summary.avg_response_time || '0h';
    document.getElementById('emailsGrowth').textContent = (summary.emails_growth || 0) + '%';
    document.getElementById('incidentsRate').textContent = (summary.incident_rate || 0).toFixed(1) + '%';
    document.getElementById('resolutionRate').textContent = (summary.resolution_rate || 0).toFixed(1) + '%';
    document.getElementById('responseImprovement').textContent = (summary.response_improvement || 0) + '%';
}

// Create all charts
function createCharts() {
    createRiskTrendChart();
    createRiskDistributionChart();
    createDepartmentVolumeChart();
    createThreatDomainsChart();
    createMLPerformanceChart();
    createResponseTimeChart();
    createPolicyEffectivenessChart();
}

// Risk trend chart (line chart)
function createRiskTrendChart() {
    const ctx = document.getElementById('riskTrendChart').getContext('2d');
    
    if (charts.riskTrend) {
        charts.riskTrend.destroy();
    }
    
    const trendData = reportData.risk_trends || {};
    
    charts.riskTrend = new Chart(ctx, {
        type: 'line',
        data: {
            labels: trendData.labels || [],
            datasets: [
                {
                    label: 'Critical Risk',
                    data: trendData.critical || [],
                    borderColor: '#dc3545',
                    backgroundColor: 'rgba(220, 53, 69, 0.1)',
                    fill: false,
                    tension: 0.3
                },
                {
                    label: 'High Risk',
                    data: trendData.high || [],
                    borderColor: '#fd7e14',
                    backgroundColor: 'rgba(253, 126, 20, 0.1)',
                    fill: false,
                    tension: 0.3
                },
                {
                    label: 'Medium Risk',
                    data: trendData.medium || [],
                    borderColor: '#ffc107',
                    backgroundColor: 'rgba(255, 193, 7, 0.1)',
                    fill: false,
                    tension: 0.3
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    title: {
                        display: true,
                        text: 'Number of Cases'
                    }
                },
                x: {
                    title: {
                        display: true,
                        text: 'Time Period'
                    }
                }
            }
        }
    });
}

// Risk distribution chart (doughnut)
function createRiskDistributionChart() {
    const ctx = document.getElementById('riskDistributionChart').getContext('2d');
    
    if (charts.riskDistribution) {
        charts.riskDistribution.destroy();
    }
    
    const distribution = reportData.risk_distribution || {};
    
    charts.riskDistribution = new Chart(ctx, {
        type: 'doughnut',
        data: {
            labels: ['Critical', 'High', 'Medium', 'Low'],
            datasets: [{
                data: [
                    distribution.critical || 0,
                    distribution.high || 0,
                    distribution.medium || 0,
                    distribution.low || 0
                ],
                backgroundColor: ['#dc3545', '#fd7e14', '#ffc107', '#28a745'],
                hoverBackgroundColor: ['#c82333', '#e8690b', '#e0a800', '#1e7e34']
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'bottom'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = ((context.raw / total) * 100).toFixed(1);
                            return `${context.label}: ${context.raw} (${percentage}%)`;
                        }
                    }
                }
            }
        }
    });
}

// Department volume chart (bar)
function createDepartmentVolumeChart() {
    const ctx = document.getElementById('departmentVolumeChart').getContext('2d');
    
    if (charts.departmentVolume) {
        charts.departmentVolume.destroy();
    }
    
    const volumeData = reportData.department_volume || {};
    
    charts.departmentVolume = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: volumeData.labels || [],
            datasets: [{
                label: 'Email Volume',
                data: volumeData.data || [],
                backgroundColor: '#4e73df',
                borderColor: '#2e59d9',
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
                    title: {
                        display: true,
                        text: 'Number of Emails'
                    }
                }
            }
        }
    });
}

// Threat domains chart (horizontal bar)
function createThreatDomainsChart() {
    const ctx = document.getElementById('threatDomainsChart').getContext('2d');
    
    if (charts.threatDomains) {
        charts.threatDomains.destroy();
    }
    
    const threatData = reportData.threat_domains || {};
    
    charts.threatDomains = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: threatData.labels || [],
            datasets: [{
                label: 'Threat Count',
                data: threatData.data || [],
                backgroundColor: '#e74a3b',
                borderColor: '#dc3545',
                borderWidth: 1
            }]
        },
        options: {
            indexAxis: 'y',
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
                    title: {
                        display: true,
                        text: 'Number of Threats'
                    }
                }
            }
        }
    });
}

// ML Performance chart (radar)
function createMLPerformanceChart() {
    const ctx = document.getElementById('mlPerformanceChart').getContext('2d');
    
    if (charts.mlPerformance) {
        charts.mlPerformance.destroy();
    }
    
    const mlData = reportData.ml_performance || {};
    
    charts.mlPerformance = new Chart(ctx, {
        type: 'radar',
        data: {
            labels: ['Accuracy', 'Precision', 'Recall', 'F1-Score', 'Specificity'],
            datasets: [{
                label: 'Current Period',
                data: [
                    mlData.accuracy || 0,
                    mlData.precision || 0,
                    mlData.recall || 0,
                    mlData.f1_score || 0,
                    mlData.specificity || 0
                ],
                borderColor: '#4e73df',
                backgroundColor: 'rgba(78, 115, 223, 0.2)',
                pointBackgroundColor: '#4e73df'
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
                r: {
                    beginAtZero: true,
                    max: 100,
                    ticks: {
                        stepSize: 20
                    }
                }
            }
        }
    });
    
    // Update performance metrics
    document.getElementById('mlAccuracy').textContent = (mlData.accuracy || 0).toFixed(1) + '%';
    document.getElementById('mlPrecision').textContent = (mlData.precision || 0).toFixed(1) + '%';
    document.getElementById('mlRecall').textContent = (mlData.recall || 0).toFixed(1) + '%';
}

// Response time chart (bar)
function createResponseTimeChart() {
    const ctx = document.getElementById('responseTimeChart').getContext('2d');
    
    if (charts.responseTime) {
        charts.responseTime.destroy();
    }
    
    const responseData = reportData.response_times || {};
    
    charts.responseTime = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: responseData.labels || [],
            datasets: [{
                label: 'Average Response Time (hours)',
                data: responseData.data || [],
                backgroundColor: '#17a2b8',
                borderColor: '#138496',
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
                    title: {
                        display: true,
                        text: 'Hours'
                    }
                }
            }
        }
    });
}

// Policy effectiveness chart (line)
function createPolicyEffectivenessChart() {
    const ctx = document.getElementById('policyEffectivenessChart').getContext('2d');
    
    if (charts.policyEffectiveness) {
        charts.policyEffectiveness.destroy();
    }
    
    const policyData = reportData.policy_effectiveness || {};
    
    charts.policyEffectiveness = new Chart(ctx, {
        type: 'line',
        data: {
            labels: policyData.labels || [],
            datasets: [{
                label: 'Detection Rate (%)',
                data: policyData.detection_rate || [],
                borderColor: '#28a745',
                backgroundColor: 'rgba(40, 167, 69, 0.1)',
                fill: true,
                tension: 0.3
            }, {
                label: 'False Positive Rate (%)',
                data: policyData.false_positive_rate || [],
                borderColor: '#dc3545',
                backgroundColor: 'rgba(220, 53, 69, 0.1)',
                fill: true,
                tension: 0.3
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    max: 100,
                    title: {
                        display: true,
                        text: 'Percentage'
                    }
                }
            }
        }
    });
}

// Render top risks table
function renderTopRisksTable() {
    const tbody = document.getElementById('topRisksTableBody');
    const topRisks = reportData.top_risks || [];
    
    tbody.innerHTML = '';
    
    topRisks.forEach(risk => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><span class="badge bg-warning">${risk.category}</span></td>
            <td><strong>${risk.count}</strong></td>
            <td>${risk.avg_score.toFixed(2)}</td>
            <td>${risk.top_domain}</td>
            <td>
                <div class="progress" style="height: 20px;">
                    <div class="progress-bar bg-success" style="width: ${risk.resolution_rate}%">
                        ${risk.resolution_rate.toFixed(1)}%
                    </div>
                </div>
            </td>
            <td>
                <i class="fas fa-arrow-${risk.trend === 'up' ? 'up trend-up' : risk.trend === 'down' ? 'down trend-down' : 'right trend-stable'}"></i>
                ${risk.trend_percentage}%
            </td>
            <td>
                <span class="badge bg-${risk.action_priority === 'high' ? 'danger' : risk.action_priority === 'medium' ? 'warning' : 'info'}">
                    ${risk.action_required}
                </span>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Render recommendations
function renderRecommendations() {
    const securityRecs = document.getElementById('securityRecommendations');
    const processRecs = document.getElementById('processRecommendations');
    
    const recommendations = reportData.recommendations || {};
    
    // Security recommendations
    securityRecs.innerHTML = '';
    (recommendations.security || []).forEach(rec => {
        const li = document.createElement('li');
        li.className = 'recommendation-item';
        li.innerHTML = `
            <i class="fas fa-shield-alt text-primary me-2"></i>
            <strong>${rec.title}</strong><br>
            <small class="text-muted">${rec.description}</small>
        `;
        securityRecs.appendChild(li);
    });
    
    // Process recommendations
    processRecs.innerHTML = '';
    (recommendations.process || []).forEach(rec => {
        const li = document.createElement('li');
        li.className = 'recommendation-item';
        li.innerHTML = `
            <i class="fas fa-cogs text-success me-2"></i>
            <strong>${rec.title}</strong><br>
            <small class="text-muted">${rec.description}</small>
        `;
        processRecs.appendChild(li);
    });
}

// Show all report sections
function showReportSections() {
    document.getElementById('summaryCards').style.display = 'block';
    document.getElementById('mainCharts').style.display = 'block';
    document.getElementById('secondaryCharts').style.display = 'block';
    document.getElementById('detailedAnalytics').style.display = 'block';
    document.getElementById('topRisksSection').style.display = 'block';
    document.getElementById('recommendationsSection').style.display = 'block';
}

// Hide all report sections
function hideReportSections() {
    document.getElementById('summaryCards').style.display = 'none';
    document.getElementById('mainCharts').style.display = 'none';
    document.getElementById('secondaryCharts').style.display = 'none';
    document.getElementById('detailedAnalytics').style.display = 'none';
    document.getElementById('topRisksSection').style.display = 'none';
    document.getElementById('recommendationsSection').style.display = 'none';
}

// Export functions
function exportMonthlyReport() {
    if (selectedSessionIds.size === 0) {
        showNotification('Please generate a report first', 'warning');
        return;
    }
    
    showLoading('Generating PDF report...');
    
    fetch('/api/monthly-report/export-pdf', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_ids: Array.from(selectedSessionIds),
            report_data: reportData
        })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `monthly_report_${new Date().toISOString().slice(0, 10)}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        hideLoading();
        showNotification('PDF report downloaded', 'success');
    })
    .catch(error => {
        console.error('Error exporting PDF:', error);
        hideLoading();
        showNotification('Error exporting PDF report', 'error');
    });
}

function exportExcelReport() {
    if (selectedSessionIds.size === 0) {
        showNotification('Please generate a report first', 'warning');
        return;
    }
    
    showLoading('Generating Excel report...');
    
    fetch('/api/monthly-report/export-excel', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_ids: Array.from(selectedSessionIds),
            report_data: reportData
        })
    })
    .then(response => response.blob())
    .then(blob => {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `monthly_report_${new Date().toISOString().slice(0, 10)}.xlsx`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);
        hideLoading();
        showNotification('Excel report downloaded', 'success');
    })
    .catch(error => {
        console.error('Error exporting Excel:', error);
        hideLoading();
        showNotification('Error exporting Excel report', 'error');
    });
}

// Utility functions
function getStatusBadgeColor(status) {
    switch(status) {
        case 'completed': return 'success';
        case 'processing': return 'warning';
        case 'error': return 'danger';
        default: return 'secondary';
    }
}

function animateCounter(elementId, targetValue, duration = 1000) {
    const element = document.getElementById(elementId);
    if (!element) return;
    
    let startValue = 0;
    const startTime = performance.now();
    
    function updateCounter(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const currentValue = Math.floor(startValue + (targetValue - startValue) * easeOut);
        
        element.textContent = currentValue.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(updateCounter);
        } else {
            element.textContent = targetValue.toLocaleString();
        }
    }
    
    requestAnimationFrame(updateCounter);
}

function refreshDashboard() {
    location.reload();
}

function showLoading(message) {
    const loadingDiv = document.createElement('div');
    loadingDiv.id = 'loading-overlay';
    loadingDiv.innerHTML = `
        <div class="d-flex justify-content-center align-items-center" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 9999;">
            <div class="bg-white p-4 rounded">
                <div class="spinner-border text-primary me-2" role="status"></div>
                ${message}
            </div>
        </div>
    `;
    document.body.appendChild(loadingDiv);
}

function hideLoading() {
    const loadingDiv = document.getElementById('loading-overlay');
    if (loadingDiv) {
        loadingDiv.remove();
    }
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}
