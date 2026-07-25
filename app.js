// Fully Functional Dynamic Dashboard Engine
// Connects 15,000 dataset records directly to Filters, KPIs, Charts, and Table

let fullUserData = [];
let macroData = [
    { period: "2021-01", users: 1.2, gain: 4.8 },
    { period: "2022-01", users: 5.4, gain: 12.3 },
    { period: "2023-01", users: 18.5, gain: 28.6 },
    { period: "2024-01", users: 45.2, gain: 45.1 },
    { period: "2025-01", users: 78.9, gain: 58.4 },
    { period: "2026-06", users: 103.9, gain: 71.1 }
];

let chartToolsInstance = null;
let chartMacroInstance = null;
let chartIndustryInstance = null;
let chartExpInstance = null;

// Global Chart.js Minimalist Theme Defaults
Chart.defaults.font.family = "'Inter', -apple-system, sans-serif";
Chart.defaults.font.size = 11;
Chart.defaults.color = "#64748b";

document.addEventListener('DOMContentLoaded', async () => {
    initCharts();
    await loadData();
    setupEventListeners();
});

async function loadData() {
    try {
        const response = await fetch('data/user_level_ai_adoption_enriched.csv');
        if (!response.ok) throw new Error("Failed to load CSV");
        const csvText = await response.text();
        fullUserData = parseCSV(csvText);
        
        console.log(`Loaded ${fullUserData.length} records dynamically.`);
        applyFilters();
    } catch (err) {
        console.warn("CSV Fetch fallback triggered:", err);
    }
}

function parseCSV(text) {
    const lines = text.trim().split(/\r?\n/);
    if (lines.length < 2) return [];
    
    const headers = lines[0].split(',').map(h => h.trim());
    const data = [];
    
    for (let i = 1; i < lines.length; i++) {
        if (!lines[i].trim()) continue;
        const vals = lines[i].split(',').map(v => v.trim());
        const row = {};
        headers.forEach((h, idx) => {
            row[h] = vals[idx];
        });
        
        // Parse numerical fields
        row.Experience_Years = parseInt(row.Experience_Years) || 0;
        row.Daily_Token_Usage = parseInt(row.Daily_Token_Usage) || 0;
        row.Tasks_Automated_Per_Week = parseInt(row.Tasks_Automated_Per_Week) || 0;
        row.Productivity_Gain_Percent = parseFloat(row.Productivity_Gain_Percent) || 0;
        
        data.push(row);
    }
    return data;
}

function getFilteredData() {
    const indFilter = document.getElementById('filter-industry').value;
    const toolFilter = document.getElementById('filter-tool').value;
    const locFilter = document.getElementById('filter-location').value;
    const expFilter = document.getElementById('filter-experience').value;
    const searchTerm = document.getElementById('table-search').value.toLowerCase();

    return fullUserData.filter(row => {
        if (indFilter !== 'ALL' && row.Industry !== indFilter) return false;
        if (toolFilter !== 'ALL' && row.Primary_AI_Tool !== toolFilter) return false;
        if (locFilter !== 'ALL' && row.Location !== locFilter) return false;
        if (expFilter !== 'ALL' && row.Experience_Group !== expFilter) return false;
        
        if (searchTerm) {
            const searchHaystack = `${row.User_ID} ${row.Industry} ${row.Job_Role} ${row.Location} ${row.Primary_AI_Tool}`.toLowerCase();
            if (!searchHaystack.includes(searchTerm)) return false;
        }
        return true;
    });
}

function applyFilters() {
    const filtered = getFilteredData();
    
    updateKPIs(filtered);
    updateCharts(filtered);
    renderTable(filtered.slice(0, 50)); // Render top 50 filtered rows
}

function updateKPIs(data) {
    const count = data.length;
    document.getElementById('kpi-users').innerText = count.toLocaleString();

    if (count === 0) {
        document.getElementById('kpi-tokens').innerText = '0';
        document.getElementById('kpi-tasks').innerText = '0';
        document.getElementById('kpi-gain').innerText = '0%';
        return;
    }

    const totalTokens = data.reduce((sum, r) => sum + r.Daily_Token_Usage, 0);
    const totalTasks = data.reduce((sum, r) => sum + r.Tasks_Automated_Per_Week, 0);
    const totalGain = data.reduce((sum, r) => sum + r.Productivity_Gain_Percent, 0);

    const avgTokens = Math.round(totalTokens / count);
    const avgTasks = (totalTasks / count).toFixed(2);
    const avgGain = (totalGain / count).toFixed(1);

    document.getElementById('kpi-tokens').innerText = avgTokens.toLocaleString();
    document.getElementById('kpi-tasks').innerText = avgTasks;
    document.getElementById('kpi-gain').innerText = `${avgGain}%`;
}

function initCharts() {
    // 1. Chart Tools
    const ctxTools = document.getElementById('chart-tools').getContext('2d');
    chartToolsInstance = new Chart(ctxTools, {
        type: 'bar',
        data: { labels: [], datasets: [] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#94a3b8', usePointStyle: true, boxWidth: 8, font: { size: 10 } } } },
            scales: {
                x: { ticks: { color: '#94a3b8', font: { size: 10 }, maxRotation: 45, autoSkip: true }, grid: { color: '#1a2438' } },
                y: { type: 'linear', position: 'left', ticks: { color: '#38bdf8', font: { size: 10 } }, grid: { color: '#1a2438' } },
                y1: { type: 'linear', position: 'right', ticks: { color: '#34d399', font: { size: 10 } }, grid: { drawOnChartArea: false } }
            }
        }
    });

    // 2. Chart Macro Trend
    const ctxMacro = document.getElementById('chart-macro').getContext('2d');
    chartMacroInstance = new Chart(ctxMacro, {
        type: 'line',
        data: {
            labels: macroData.map(d => d.period),
            datasets: [
                {
                    label: 'Global Active Users (M)',
                    data: macroData.map(d => d.users),
                    borderColor: '#818cf8',
                    backgroundColor: 'rgba(129, 140, 248, 0.08)',
                    fill: true,
                    tension: 0.3,
                    borderWidth: 2
                },
                {
                    label: 'Avg Productivity Gain (%)',
                    data: macroData.map(d => d.gain),
                    borderColor: '#34d399',
                    borderDash: [4, 4],
                    tension: 0.3,
                    borderWidth: 2
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { labels: { color: '#94a3b8', usePointStyle: true, boxWidth: 8, font: { size: 10 } } } },
            scales: {
                x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1a2438' } },
                y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1a2438' } }
            }
        }
    });

    // 3. Chart Industry
    const ctxIndustry = document.getElementById('chart-industry').getContext('2d');
    chartIndustryInstance = new Chart(ctxIndustry, {
        type: 'bar',
        data: { labels: [], datasets: [] },
        options: {
            indexAxis: 'y',
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1a2438' } },
                y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1a2438' } }
            }
        }
    });

    // 4. Chart Experience
    const ctxExp = document.getElementById('chart-experience').getContext('2d');
    chartExpInstance = new Chart(ctxExp, {
        type: 'bar',
        data: { labels: [], datasets: [] },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                x: { ticks: { color: '#94a3b8', font: { size: 10 }, maxRotation: 45, autoSkip: true }, grid: { color: '#1a2438' } },
                y: { ticks: { color: '#94a3b8', font: { size: 10 } }, grid: { color: '#1a2438' } }
            }
        }
    });
}

function updateCharts(data) {
    // 1. Tool Aggregations
    const toolGroups = {};
    data.forEach(r => {
        const t = r.Primary_AI_Tool;
        if (!toolGroups[t]) toolGroups[t] = { count: 0, sumGain: 0 };
        toolGroups[t].count += 1;
        toolGroups[t].sumGain += r.Productivity_Gain_Percent;
    });

    const toolLabels = Object.keys(toolGroups).sort((a, b) => toolGroups[b].count - toolGroups[a].count);
    const toolCounts = toolLabels.map(t => toolGroups[t].count);
    const toolGains = toolLabels.map(t => (toolGroups[t].sumGain / toolGroups[t].count).toFixed(1));

    chartToolsInstance.data = {
        labels: toolLabels,
        datasets: [
            {
                label: 'User Sample Count',
                data: toolCounts,
                backgroundColor: 'rgba(56, 189, 248, 0.15)',
                borderColor: '#38bdf8',
                borderWidth: 1,
                borderRadius: 4,
                yAxisID: 'y'
            },
            {
                label: 'Avg Productivity Gain (%)',
                data: toolGains,
                type: 'line',
                borderColor: '#34d399',
                backgroundColor: '#34d399',
                borderWidth: 2,
                pointRadius: 4,
                yAxisID: 'y1'
            }
        ]
    };
    chartToolsInstance.update();

    // 2. Industry Aggregations
    const indGroups = {};
    data.forEach(r => {
        const ind = r.Industry;
        if (!indGroups[ind]) indGroups[ind] = { count: 0, sumGain: 0 };
        indGroups[ind].count += 1;
        indGroups[ind].sumGain += r.Productivity_Gain_Percent;
    });

    const indLabels = Object.keys(indGroups).sort((a, b) => (indGroups[b].sumGain / indGroups[b].count) - (indGroups[a].sumGain / indGroups[a].count));
    const indGains = indLabels.map(ind => (indGroups[ind].sumGain / indGroups[ind].count).toFixed(1));

    chartIndustryInstance.data = {
        labels: indLabels,
        datasets: [{
            label: 'Avg Productivity Gain (%)',
            data: indGains,
            backgroundColor: 'rgba(56, 189, 248, 0.2)',
            borderColor: '#38bdf8',
            borderWidth: 1,
            borderRadius: 4
        }]
    };
    chartIndustryInstance.update();

    // 3. Experience Aggregations
    const expGroups = {};
    data.forEach(r => {
        const eg = r.Experience_Group || 'Other';
        if (!expGroups[eg]) expGroups[eg] = { count: 0, sumGain: 0 };
        expGroups[eg].count += 1;
        expGroups[eg].sumGain += r.Productivity_Gain_Percent;
    });

    const expLabels = ['Junior (0-3 yrs)', 'Mid-Level (4-8 yrs)', 'Senior (9-15 yrs)', 'Veteran (>15 yrs)'].filter(l => expGroups[l]);
    const expGains = expLabels.map(eg => (expGroups[eg].sumGain / expGroups[eg].count).toFixed(1));

    chartExpInstance.data = {
        labels: expLabels,
        datasets: [{
            label: 'Avg Productivity Gain (%)',
            data: expGains,
            backgroundColor: 'rgba(129, 140, 248, 0.2)',
            borderColor: '#818cf8',
            borderWidth: 1,
            borderRadius: 4
        }]
    };
    chartExpInstance.update();
}

function renderTable(data) {
    const tbody = document.getElementById('table-body');
    tbody.innerHTML = '';

    if (data.length === 0) {
        tbody.innerHTML = `<tr><td colspan="9" style="text-align: center; color: #64748b; padding: 20px;">No matching user records found</td></tr>`;
        return;
    }
    
    data.forEach(user => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td><code>${user.User_ID}</code></td>
            <td>${user.Industry}</td>
            <td>${user.Job_Role}</td>
            <td>${user.Location}</td>
            <td>${user.Experience_Years} yrs</td>
            <td><strong>${user.Primary_AI_Tool}</strong></td>
            <td>${user.Daily_Token_Usage.toLocaleString()}</td>
            <td>${user.Tasks_Automated_Per_Week}</td>
            <td><span style="color: #34d399; font-weight: 600;">${user.Productivity_Gain_Percent.toFixed(1)}%</span></td>
        `;
        tbody.appendChild(tr);
    });
}

function setupEventListeners() {
    const filterIds = ['filter-industry', 'filter-tool', 'filter-location', 'filter-experience'];
    filterIds.forEach(id => {
        document.getElementById(id).addEventListener('change', applyFilters);
    });

    document.getElementById('table-search').addEventListener('input', applyFilters);

    document.getElementById('reset-filters').addEventListener('click', () => {
        filterIds.forEach(id => {
            document.getElementById(id).value = 'ALL';
        });
        document.getElementById('table-search').value = '';
        applyFilters();
    });

    setupMobileDrawer();
}

function setupMobileDrawer() {
    const mobileToggle = document.getElementById('mobile-menu-toggle');
    const closeSidebarBtn = document.getElementById('close-sidebar');
    const backdrop = document.getElementById('sidebar-backdrop');
    const sidebar = document.getElementById('sidebar');

    function openDrawer() {
        sidebar?.classList.add('open');
        backdrop?.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    function closeDrawer() {
        sidebar?.classList.remove('open');
        backdrop?.classList.remove('active');
        document.body.style.overflow = '';
    }

    if (mobileToggle) mobileToggle.addEventListener('click', openDrawer);
    if (closeSidebarBtn) closeSidebarBtn.addEventListener('click', closeDrawer);
    if (backdrop) backdrop.addEventListener('click', closeDrawer);

    window.addEventListener('resize', () => {
        if (window.innerWidth > 900) {
            closeDrawer();
        }
        chartToolsInstance?.resize();
        chartMacroInstance?.resize();
        chartIndustryInstance?.resize();
        chartExpInstance?.resize();
    });
}
