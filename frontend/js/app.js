/**
 * Unst2st 前端交互逻辑
 */

// API基础URL（生产环境需要修改）
const API_BASE_URL = window.location.origin.includes('localhost')
    ? 'http://localhost:8000'
    : window.location.origin;

// 全局状态
let currentTemplate = null;
let selectedFiles = [];
let templates = [];

// ==================== 工具函数 ====================

// 显示Toast通知
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = `toast toast-${type} show`;
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// API请求封装
async function apiRequest(endpoint, options = {}) {
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, {
            ...options,
            headers: {
                ...options.headers,
            }
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || '请求失败');
        }

        return await response.json();
    } catch (error) {
        console.error('API请求错误:', error);
        throw error;
    }
}

// ==================== 模板管理 ====================

// 加载所有模板
async function loadTemplates() {
    try {
        templates = await apiRequest('/api/templates');
        const select = document.getElementById('template-select');
        select.innerHTML = '<option value="">-- 请选择模板 --</option>';

        templates.forEach(template => {
            const option = document.createElement('option');
            option.value = template.id;
            option.textContent = template.name;
            select.appendChild(option);
        });
    } catch (error) {
        showToast('加载模板失败: ' + error.message, 'error');
    }
}

// 显示模板编辑器
function showTemplateEditor(template = null) {
    const editor = document.getElementById('template-editor');
    const display = document.getElementById('current-template-display');

    editor.style.display = 'block';
    display.style.display = 'none';

    const nameInput = document.getElementById('template-name');
    const fieldsContainer = document.getElementById('fields-container');

    if (template) {
        nameInput.value = template.name;
        fieldsContainer.innerHTML = '';
        template.fields.forEach(field => {
            addFieldRow(field.name, field.description);
        });
    } else {
        nameInput.value = '';
        fieldsContainer.innerHTML = '';
        addFieldRow(); // 添加一个空字段
    }
}

// 添加字段行
function addFieldRow(name = '', description = '') {
    const container = document.getElementById('fields-container');
    const fieldDiv = document.createElement('div');
    fieldDiv.className = 'field-row';
    fieldDiv.innerHTML = `
        <input type="text" class="field-name" placeholder="字段名称（如：公司名称）" value="${name}">
        <input type="text" class="field-desc" placeholder="字段描述（如：合作方公司全称）" value="${description}">
        <button class="btn btn-danger btn-small remove-field-btn">删除</button>
    `;
    container.appendChild(fieldDiv);

    // 绑定删除按钮事件
    fieldDiv.querySelector('.remove-field-btn').addEventListener('click', () => {
        fieldDiv.remove();
    });
}

// 保存模板
async function saveTemplate() {
    const name = document.getElementById('template-name').value.trim();
    if (!name) {
        showToast('请输入模板名称', 'error');
        return;
    }

    const fieldRows = document.querySelectorAll('.field-row');
    const fields = [];

    fieldRows.forEach(row => {
        const fieldName = row.querySelector('.field-name').value.trim();
        const fieldDesc = row.querySelector('.field-desc').value.trim();
        if (fieldName) {
            fields.push({
                name: fieldName,
                description: fieldDesc
            });
        }
    });

    if (fields.length === 0) {
        showToast('请至少添加一个字段', 'error');
        return;
    }

    try {
        const template = await apiRequest('/api/templates', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name, fields })
        });

        showToast('模板保存成功', 'success');
        currentTemplate = template;
        await loadTemplates();
        showCurrentTemplate();
    } catch (error) {
        showToast('保存模板失败: ' + error.message, 'error');
    }
}

// 加载选中的模板
async function loadSelectedTemplate() {
    const select = document.getElementById('template-select');
    const templateId = select.value;

    if (!templateId) {
        showToast('请选择一个模板', 'error');
        return;
    }

    try {
        currentTemplate = await apiRequest(`/api/templates/${templateId}`);
        showCurrentTemplate();
        showToast('模板加载成功', 'success');
    } catch (error) {
        showToast('加载模板失败: ' + error.message, 'error');
    }
}

// 显示当前模板
function showCurrentTemplate() {
    const editor = document.getElementById('template-editor');
    const display = document.getElementById('current-template-display');
    const info = document.getElementById('current-template-info');

    editor.style.display = 'none';
    display.style.display = 'block';

    let html = `<h4>${currentTemplate.name}</h4><ul>`;
    currentTemplate.fields.forEach(field => {
        html += `<li><strong>${field.name}</strong>`;
        if (field.description) {
            html += ` - ${field.description}`;
        }
        html += `</li>`;
    });
    html += `</ul>`;
    info.innerHTML = html;

    // 显示上传区域
    document.getElementById('upload-section').style.display = 'block';
}

// 删除模板
async function deleteTemplate() {
    const select = document.getElementById('template-select');
    const templateId = select.value;

    if (!templateId) {
        showToast('请选择要删除的模板', 'error');
        return;
    }

    if (!confirm('确定要删除这个模板吗？')) {
        return;
    }

    try {
        await apiRequest(`/api/templates/${templateId}`, {
            method: 'DELETE'
        });
        showToast('模板已删除', 'success');
        await loadTemplates();
        currentTemplate = null;
        document.getElementById('current-template-display').style.display = 'none';
    } catch (error) {
        showToast('删除模板失败: ' + error.message, 'error');
    }
}

// ==================== 文件上传 ====================

// 处理文件选择
function handleFileSelect(files) {
    selectedFiles = Array.from(files);

    if (selectedFiles.length === 0) {
        document.getElementById('file-list').style.display = 'none';
        document.getElementById('extract-btn').style.display = 'none';
        return;
    }

    const fileList = document.getElementById('file-list');
    const fileItems = document.getElementById('file-items');

    fileItems.innerHTML = '';
    selectedFiles.forEach((file, index) => {
        const li = document.createElement('li');
        li.innerHTML = `
            <span>📄 ${file.name} (${(file.size / 1024).toFixed(2)} KB)</span>
            <button class="btn btn-danger btn-small" onclick="removeFile(${index})">删除</button>
        `;
        fileItems.appendChild(li);
    });

    fileList.style.display = 'block';
    document.getElementById('extract-btn').style.display = 'block';
}

// 删除文件
function removeFile(index) {
    selectedFiles.splice(index, 1);
    handleFileSelect(selectedFiles);
}

// 提取信息
async function extractInformation() {
    if (!currentTemplate) {
        showToast('请先选择或创建一个模板', 'error');
        return;
    }

    if (selectedFiles.length === 0) {
        showToast('请先上传文件', 'error');
        return;
    }

    const formData = new FormData();
    formData.append('template_id', currentTemplate.id);
    selectedFiles.forEach(file => {
        formData.append('files', file);
    });

    const loading = document.getElementById('loading');
    const extractBtn = document.getElementById('extract-btn');

    loading.style.display = 'block';
    extractBtn.disabled = true;

    try {
        const result = await apiRequest('/api/extract', {
            method: 'POST',
            body: formData
        });

        loading.style.display = 'none';
        extractBtn.disabled = false;

        if (result.success) {
            showToast(result.message, 'success');
            displayResults(result.data);
        } else {
            showToast('提取失败: ' + result.message, 'error');
        }
    } catch (error) {
        loading.style.display = 'none';
        extractBtn.disabled = false;
        showToast('提取失败: ' + error.message, 'error');
    }
}

// ==================== 结果展示 ====================

// 显示提取结果
function displayResults(data) {
    const resultSection = document.getElementById('result-section');
    const tableHeader = document.getElementById('table-header');
    const tableBody = document.getElementById('table-body');

    resultSection.style.display = 'block';

    // 构建表头（所有字段 + 文件名）
    tableHeader.innerHTML = '';
    const allFields = ['文件名', ...currentTemplate.fields.map(f => f.name)];

    allFields.forEach(field => {
        const th = document.createElement('th');
        th.textContent = field;
        tableHeader.appendChild(th);
    });

    // 构建表格数据
    tableBody.innerHTML = '';
    data.forEach(row => {
        const tr = document.createElement('tr');

        allFields.forEach(field => {
            const td = document.createElement('td');
            td.textContent = row[field] || '';
            td.contentEditable = true;
            td.className = 'editable-cell';
            tr.appendChild(td);
        });

        tableBody.appendChild(tr);
    });

    // 滚动到结果区域
    resultSection.scrollIntoView({ behavior: 'smooth' });
}

// 复制表格
function copyTable() {
    const table = document.getElementById('result-table');

    let text = '';
    const rows = table.querySelectorAll('tr');
    rows.forEach(row => {
        const cells = row.querySelectorAll('th, td');
        const rowText = Array.from(cells).map(cell => cell.textContent).join('\t');
        text += rowText + '\n';
    });

    navigator.clipboard.writeText(text).then(() => {
        showToast('表格已复制到剪贴板', 'success');
    }).catch(() => {
        showToast('复制失败，请手动选择复制', 'error');
    });
}

// 重新开始
function resetApp() {
    if (confirm('确定要重新开始吗？当前结果将被清空。')) {
        selectedFiles = [];
        document.getElementById('file-list').style.display = 'none';
        document.getElementById('extract-btn').style.display = 'none';
        document.getElementById('result-section').style.display = 'none';
        document.getElementById('file-input').value = '';
        showToast('已重置', 'info');
    }
}

// ==================== 事件绑定 ====================

document.addEventListener('DOMContentLoaded', () => {
    // 加载模板列表
    loadTemplates();

    // 模板管理按钮
    document.getElementById('new-template-btn').addEventListener('click', () => {
        showTemplateEditor();
    });

    document.getElementById('add-field-btn').addEventListener('click', () => {
        addFieldRow();
    });

    document.getElementById('save-template-btn').addEventListener('click', saveTemplate);

    document.getElementById('load-template-btn').addEventListener('click', loadSelectedTemplate);

    document.getElementById('delete-template-btn').addEventListener('click', deleteTemplate);

    // 文件上传
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');

    uploadArea.addEventListener('click', () => {
        fileInput.click();
    });

    fileInput.addEventListener('change', (e) => {
        handleFileSelect(e.target.files);
    });

    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        handleFileSelect(e.dataTransfer.files);
    });

    // 提取按钮
    document.getElementById('extract-btn').addEventListener('click', extractInformation);

    // 结果操作按钮
    document.getElementById('copy-table-btn').addEventListener('click', copyTable);
    document.getElementById('reset-btn').addEventListener('click', resetApp);
});
