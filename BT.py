/*
 * Hệ Thống Quản Lý Dự Án - Phiên bản có thể nhập dữ liệu
 * @author Admin
 */

import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.text.SimpleDateFormat;
import java.util.Date;

// Data classes
class Project {
    String id, name, client, startDate, endDate, status, progress;
    
    public Project(String id, String name, String client, String startDate, String endDate, String status, String progress) {
        this.id = id;
        this.name = name;
        this.client = client;
        this.startDate = startDate;
        this.endDate = endDate;
        this.status = status;
        this.progress = progress;
    }
    
    public Object[] toArray() {
        return new Object[]{id, name, client, startDate, endDate, status, progress};
    }
}

class Task {
    String id, name, project, assignee, priority, dueDate, status;
    
    public Task(String id, String name, String project, String assignee, String priority, String dueDate, String status) {
        this.id = id;
        this.name = name;
        this.project = project;
        this.assignee = assignee;
        this.priority = priority;
        this.dueDate = dueDate;
        this.status = status;
    }
    
    public Object[] toArray() {
        return new Object[]{id, name, project, assignee, priority, dueDate, status};
    }
}

class Employee {
    String id, name, position, email, phone, department, status;
    
    public Employee(String id, String name, String position, String email, String phone, String department, String status) {
        this.id = id;
        this.name = name;
        this.position = position;
        this.email = email;
        this.phone = phone;
        this.department = department;
        this.status = status;
    }
    
    public Object[] toArray() {
        return new Object[]{id, name, position, email, phone, department, status};
    }
}

// Main Dashboard Panel
public class MainDashboard extends JFrame {
    private JPanel sidebarPanel;
    private JPanel contentPanel;
    private CardLayout contentLayout;
    private JLabel userLabel;
    private String currentUser = "Admin";
    
    // Data storage
    private ArrayList<Project> projects = new ArrayList<>();
    private ArrayList<Task> tasks = new ArrayList<>();
    private ArrayList<Employee> employees = new ArrayList<>();
    
    // Table models
    private DefaultTableModel projectTableModel;
    private DefaultTableModel taskTableModel;
    private DefaultTableModel employeeTableModel;
    
    // ID counters
    private int projectIdCounter = 1;
    private int taskIdCounter = 1;
    private int employeeIdCounter = 1;
    
    public MainDashboard() {
        initializeComponents();
        setupLayout();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        setTitle("Hệ Thống Quản Lý Dự Án");
        setVisible(true);
    }
    
    private void initializeComponents() {
        createSidebar();
        createContentPanel();
    }
    
    private void createSidebar() {
        sidebarPanel = new JPanel();
        sidebarPanel.setLayout(new BoxLayout(sidebarPanel, BoxLayout.Y_AXIS));
        sidebarPanel.setBackground(new Color(52, 73, 94));
        sidebarPanel.setPreferredSize(new Dimension(250, 0));
        
        // Header
        JPanel headerPanel = new JPanel();
        headerPanel.setBackground(new Color(44, 62, 80));
        headerPanel.setMaximumSize(new Dimension(250, 80));
        headerPanel.setLayout(new BorderLayout());
        
        JLabel titleLabel = new JLabel("QUẢN LÝ DỰ ÁN");
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 16));
        titleLabel.setHorizontalAlignment(SwingConstants.CENTER);
        headerPanel.add(titleLabel, BorderLayout.CENTER);
        
        // User info
        JPanel userPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        userPanel.setBackground(new Color(52, 73, 94));
        userPanel.setMaximumSize(new Dimension(250, 40));
        
        userLabel = new JLabel("👤 " + currentUser);
        userLabel.setForeground(Color.WHITE);
        userLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        userPanel.add(userLabel);
        
        // Menu items
        sidebarPanel.add(headerPanel);
        sidebarPanel.add(userPanel);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 20)));
        
        // Navigation buttons
        addMenuButton("🏠 Trang Chủ", "HOME");
        addMenuButton("📋 Quản Lý Dự Án", "PROJECTS");
        addMenuButton("✅ Công Việc", "TASKS");
        addMenuButton("👥 Nhân Viên", "EMPLOYEES");
        addMenuButton("📊 Báo Cáo", "REPORTS");
        addMenuButton("📈 Thống Kê", "STATISTICS");
        addMenuButton("⚙️ Cài Đặt", "SETTINGS");
        
        sidebarPanel.add(Box.createVerticalGlue());
        
        // Logout button
        JButton logoutBtn = new JButton("🚪 Đăng Xuất");
        logoutBtn.setBackground(new Color(231, 76, 60));
        logoutBtn.setForeground(Color.WHITE);
        logoutBtn.setBorder(new EmptyBorder(10, 20, 10, 20));
        logoutBtn.setMaximumSize(new Dimension(220, 40));
        logoutBtn.setAlignmentX(Component.CENTER_ALIGNMENT);
        logoutBtn.setFocusPainted(false);
        logoutBtn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        logoutBtn.addActionListener(e -> System.exit(0));
        sidebarPanel.add(logoutBtn);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 20)));
    }
    
    private void addMenuButton(String text, String panelName) {
        JButton button = new JButton(text);
        button.setBackground(new Color(52, 73, 94));
        button.setForeground(Color.WHITE);
        button.setBorder(new EmptyBorder(12, 20, 12, 20));
        button.setMaximumSize(new Dimension(230, 45));
        button.setAlignmentX(Component.LEFT_ALIGNMENT);
        button.setHorizontalAlignment(SwingConstants.LEFT);
        button.setFocusPainted(false);
        button.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(41, 128, 185));
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                button.setBackground(new Color(52, 73, 94));
            }
        });
        
        button.addActionListener(e -> {
            contentLayout.show(contentPanel, panelName);
            updateSelectedButton(button);
        });
        
        sidebarPanel.add(button);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 5)));
    }
    
    private void updateSelectedButton(JButton selectedButton) {
        for (Component comp : sidebarPanel.getComponents()) {
            if (comp instanceof JButton && !comp.equals(sidebarPanel.getComponent(sidebarPanel.getComponentCount()-2))) {
                comp.setBackground(new Color(52, 73, 94));
            }
        }
        selectedButton.setBackground(new Color(41, 128, 185));
    }
    
    private void createContentPanel() {
        contentLayout = new CardLayout();
        contentPanel = new JPanel(contentLayout);
        
        contentPanel.add(createHomePanel(), "HOME");
        contentPanel.add(createProjectsPanel(), "PROJECTS");
        contentPanel.add(createTasksPanel(), "TASKS");
        contentPanel.add(createEmployeesPanel(), "EMPLOYEES");
        contentPanel.add(createReportsPanel(), "REPORTS");
        contentPanel.add(createStatisticsPanel(), "STATISTICS");
        contentPanel.add(createSettingsPanel(), "SETTINGS");
        
        contentLayout.show(contentPanel, "HOME");
    }
    
    private JPanel createHomePanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        // Header
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(new Color(236, 240, 241));
        headerPanel.setBorder(new EmptyBorder(20, 30, 20, 30));
        
        JLabel titleLabel = new JLabel("Dashboard - Tổng Quan Hệ Thống");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(new Color(52, 73, 94));
        headerPanel.add(titleLabel, BorderLayout.WEST);
        
        JLabel dateLabel = new JLabel(new SimpleDateFormat("dd/MM/yyyy HH:mm").format(new Date()));
        dateLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        dateLabel.setForeground(Color.GRAY);
        headerPanel.add(dateLabel, BorderLayout.EAST);
        
        // Statistics cards
        JPanel statsPanel = new JPanel(new GridLayout(1, 4, 20, 0));
        statsPanel.setBorder(new EmptyBorder(30, 30, 30, 30));
        statsPanel.setBackground(Color.WHITE);
        
        statsPanel.add(createStatCard("📋 Tổng Dự Án", String.valueOf(projects.size()), new Color(52, 152, 219)));
        statsPanel.add(createStatCard("✅ Công Việc", String.valueOf(tasks.size()), new Color(46, 204, 113)));
        statsPanel.add(createStatCard("👥 Nhân Viên", String.valueOf(employees.size()), new Color(155, 89, 182)));
        
        // Count overdue tasks
        int overdueTasks = 0;
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
        Date today = new Date();
        for (Task task : tasks) {
            try {
                Date dueDate = sdf.parse(task.dueDate);
                if (dueDate.before(today) && !task.status.equals("Hoàn thành")) {
                    overdueTasks++;
                }
            } catch (Exception e) {
                // Ignore parsing error
            }
        }
        statsPanel.add(createStatCard("⏰ Quá Hạn", String.valueOf(overdueTasks), new Color(231, 76, 60)));
        
        // Recent activities placeholder
        JPanel recentPanel = new JPanel(new BorderLayout());
        recentPanel.setBorder(BorderFactory.createTitledBorder("Hoạt Động Gần Đây"));
        recentPanel.setBackground(Color.WHITE);
        
        JLabel noActivityLabel = new JLabel("Chưa có hoạt động nào", SwingConstants.CENTER);
        noActivityLabel.setFont(new Font("Arial", Font.ITALIC, 14));
        noActivityLabel.setForeground(Color.GRAY);
        noActivityLabel.setBorder(new EmptyBorder(50, 0, 50, 0));
        recentPanel.add(noActivityLabel, BorderLayout.CENTER);
        
        panel.add(headerPanel, BorderLayout.NORTH);
        
        JPanel centerPanel = new JPanel(new BorderLayout());
        centerPanel.add(statsPanel, BorderLayout.NORTH);
        centerPanel.add(recentPanel, BorderLayout.CENTER);
        panel.add(centerPanel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createStatCard(String title, String value, Color color) {
        JPanel card = new JPanel();
        card.setLayout(new BoxLayout(card, BoxLayout.Y_AXIS));
        card.setBackground(color);
        card.setBorder(new EmptyBorder(20, 20, 20, 20));
        
        JLabel titleLabel = new JLabel(title);
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel valueLabel = new JLabel(value);
        valueLabel.setForeground(Color.WHITE);
        valueLabel.setFont(new Font("Arial", Font.BOLD, 32));
        valueLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        card.add(titleLabel);
        card.add(Box.createRigidArea(new Dimension(0, 10)));
        card.add(valueLabel);
        
        return card;
    }
    
    private JPanel createProjectsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        // Header with toolbar
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        headerPanel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Quản Lý Dự Án");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerPanel.add(titleLabel, BorderLayout.WEST);
        
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        buttonPanel.setBackground(Color.WHITE);
        
        JButton addProjectBtn = new JButton("+ Thêm Dự Án");
        addProjectBtn.setBackground(new Color(46, 204, 113));
        addProjectBtn.setForeground(Color.WHITE);
        addProjectBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        addProjectBtn.setFocusPainted(false);
        addProjectBtn.addActionListener(e -> showAddProjectDialog());
        
        JButton editBtn = new JButton("✏️ Sửa");
        editBtn.setBackground(new Color(52, 152, 219));
        editBtn.setForeground(Color.WHITE);
        editBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        editBtn.setFocusPainted(false);
        
        JButton deleteBtn = new JButton("🗑️ Xóa");
        deleteBtn.setBackground(new Color(231, 76, 60));
        deleteBtn.setForeground(Color.WHITE);
        deleteBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        deleteBtn.setFocusPainted(false);
        
        buttonPanel.add(addProjectBtn);
        buttonPanel.add(editBtn);
        buttonPanel.add(deleteBtn);
        headerPanel.add(buttonPanel, BorderLayout.EAST);
        
        // Projects table
        String[] columns = {"ID", "Tên Dự Án", "Khách Hàng", "Ngày Bắt Đầu", "Ngày Kết Thúc", "Trạng Thái", "Tiến Độ (%)"};
        projectTableModel = new DefaultTableModel(columns, 0);
        
        JTable projectTable = new JTable(projectTableModel);
        projectTable.setRowHeight(35);
        projectTable.getTableHeader().setBackground(new Color(52, 73, 94));
        projectTable.getTableHeader().setForeground(Color.WHITE);
        projectTable.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        
        JScrollPane scrollPane = new JScrollPane(projectTable);
        scrollPane.setBorder(new EmptyBorder(0, 20, 20, 20));
        
        panel.add(headerPanel, BorderLayout.NORTH);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private void showAddProjectDialog() {
        JDialog dialog = new JDialog(this, "Thêm Dự Án Mới", true);
        dialog.setSize(500, 400);
        dialog.setLocationRelativeTo(this);
        
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(new EmptyBorder(20, 20, 20, 20));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.WEST;
        
        // Form fields
        JTextField nameField = new JTextField(20);
        JTextField clientField = new JTextField(20);
        JTextField startDateField = new JTextField(20);
        JTextField endDateField = new JTextField(20);
        JComboBox<String> statusCombo = new JComboBox<>(new String[]{"Mới tạo", "Đang thực hiện", "Tạm dừng", "Hoàn thành"});
        JTextField progressField = new JTextField(20);
        
        // Add components
        gbc.gridx = 0; gbc.gridy = 0;
        panel.add(new JLabel("Tên Dự Án:"), gbc);
        gbc.gridx = 1;
        panel.add(nameField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 1;
        panel.add(new JLabel("Khách Hàng:"), gbc);
        gbc.gridx = 1;
        panel.add(clientField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 2;
        panel.add(new JLabel("Ngày Bắt Đầu (dd/MM/yyyy):"), gbc);
        gbc.gridx = 1;
        panel.add(startDateField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 3;
        panel.add(new JLabel("Ngày Kết Thúc (dd/MM/yyyy):"), gbc);
        gbc.gridx = 1;
        panel.add(endDateField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 4;
        panel.add(new JLabel("Trạng Thái:"), gbc);
        gbc.gridx = 1;
        panel.add(statusCombo, gbc);
        
        gbc.gridx = 0; gbc.gridy = 5;
        panel.add(new JLabel("Tiến Độ (%):"), gbc);
        gbc.gridx = 1;
        panel.add(progressField, gbc);
        
        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JButton saveBtn = new JButton("Lưu");
        JButton cancelBtn = new JButton("Hủy");
        
        saveBtn.addActionListener(e -> {
            try {
                String id = "P" + String.format("%03d", projectIdCounter++);
                String name = nameField.getText().trim();
                String client = clientField.getText().trim();
                String startDate = startDateField.getText().trim();
                String endDate = endDateField.getText().trim();
                String status = (String) statusCombo.getSelectedItem();
                String progress = progressField.getText().trim() + "%";
                
                if (name.isEmpty() || client.isEmpty() || startDate.isEmpty() || endDate.isEmpty()) {
                    JOptionPane.showMessageDialog(dialog, "Vui lòng điền đầy đủ thông tin!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                
                Project project = new Project(id, name, client, startDate, endDate, status, progress);
                projects.add(project);
                projectTableModel.addRow(project.toArray());
                
                dialog.dispose();
                JOptionPane.showMessageDialog(this, "Thêm dự án thành công!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
                
                // Refresh home panel
                refreshHomePanel();
                
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(dialog, "Có lỗi xảy ra: " + ex.getMessage(), "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        });
        
        cancelBtn.addActionListener(e -> dialog.dispose());
        
        buttonPanel.add(saveBtn);
        buttonPanel.add(cancelBtn);
        
        gbc.gridx = 0; gbc.gridy = 6;
        gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(buttonPanel, gbc);
        
        dialog.add(panel);
        dialog.setVisible(true);
    }
    
    private JPanel createTasksPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        // Header
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        headerPanel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Quản Lý Công Việc");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerPanel.add(titleLabel, BorderLayout.WEST);
        
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        buttonPanel.setBackground(Color.WHITE);
        
        JButton addTaskBtn = new JButton("+ Thêm Công Việc");
        addTaskBtn.setBackground(new Color(46, 204, 113));
        addTaskBtn.setForeground(Color.WHITE);
        addTaskBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        addTaskBtn.setFocusPainted(false);
        addTaskBtn.addActionListener(e -> showAddTaskDialog());
        
        buttonPanel.add(addTaskBtn);
        headerPanel.add(buttonPanel, BorderLayout.EAST);
        
        // Tasks table
        String[] columns = {"ID", "Tên Công Việc", "Dự Án", "Người Thực Hiện", "Độ Ưu Tiên", "Ngày Hết Hạn", "Trạng Thái"};
        taskTableModel = new DefaultTableModel(columns, 0);
        
        JTable taskTable = new JTable(taskTableModel);
        taskTable.setRowHeight(35);
        taskTable.getTableHeader().setBackground(new Color(52, 73, 94));
        taskTable.getTableHeader().setForeground(Color.WHITE);
        taskTable.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        
        JScrollPane scrollPane = new JScrollPane(taskTable);
        scrollPane.setBorder(new EmptyBorder(0, 20, 20, 20));
        
        panel.add(headerPanel, BorderLayout.NORTH);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private void showAddTaskDialog() {
        JDialog dialog = new JDialog(this, "Thêm Công Việc Mới", true);
        dialog.setSize(500, 450);
        dialog.setLocationRelativeTo(this);
        
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(new EmptyBorder(20, 20, 20, 20));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.WEST;
        
        // Form fields
        JTextField nameField = new JTextField(20);
        JComboBox<String> projectCombo = new JComboBox<>();
        for (Project p : projects) {
            projectCombo.addItem(p.name);
        }
        
        JComboBox<String> assigneeCombo = new JComboBox<>();
        for (Employee e : employees) {
            assigneeCombo.addItem(e.name);
        }
        
        JComboBox<String> priorityCombo = new JComboBox<>(new String[]{"Thấp", "Trung bình", "Cao", "Rất cao"});
        JTextField dueDateField = new JTextField(20);
        JComboBox<String> statusCombo = new JComboBox<>(new String[]{"Chưa bắt đầu", "Đang thực hiện", "Hoàn thành"});
        
        // Add components
        gbc.gridx = 0; gbc.gridy = 0;
        panel.add(new JLabel("Tên Công Việc:"), gbc);
        gbc.gridx = 1;
        panel.add(nameField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 1;
        panel.add(new JLabel("Dự Án:"), gbc);
        gbc.gridx = 1;
        panel.add(projectCombo, gbc);
        
        gbc.gridx = 0; gbc.gridy = 2;
        panel.add(new JLabel("Người Thực Hiện:"), gbc);
        gbc.gridx = 1;
        panel.add(assigneeCombo, gbc);
        
        gbc.gridx = 0; gbc.gridy = 3;
        panel.add(new JLabel("Độ Ưu Tiên:"), gbc);
        gbc.gridx = 1;
        panel.add(priorityCombo, gbc);
        
        gbc.gridx = 0; gbc.gridy = 4;
        panel.add(new JLabel("Ngày Hết Hạn (dd/MM/yyyy):"), gbc);
        gbc.gridx = 1;
        panel.add(dueDateField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 5;
        panel.add(new JLabel("Trạng Thái:"), gbc);
        gbc.gridx = 1;
        panel.add(statusCombo, gbc);
        
        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JButton saveBtn = new JButton("Lưu");
        JButton cancelBtn = new JButton("Hủy");
        
        saveBtn.addActionListener(e -> {
            try {
                String id = "T" + String.format("%03d", taskIdCounter++);
                String name = nameField.getText().trim();
                String project = (String) projectCombo.getSelectedItem();
                String assignee = (String) assigneeCombo.getSelectedItem();
                String priority = (String) priorityCombo.getSelectedItem();
                String dueDate = dueDateField.getText().trim();
                String status = (String) statusCombo.getSelectedItem();
                
                if (name.isEmpty() || dueDate.isEmpty()) {
                    JOptionPane.showMessageDialog(dialog, "Vui lòng điền đầy đủ thông tin!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                
                Task task = new Task(id, name, project, assignee, priority, dueDate, status);
                tasks.add(task);
                taskTableModel.addRow(task.toArray());
                
                dialog.dispose();
                JOptionPane.showMessageDialog(this, "Thêm công việc thành công!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
                
                refreshHomePanel();
                
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(dialog, "Có lỗi xảy ra: " + ex.getMessage(), "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        });
        
        cancelBtn.addActionListener(e -> dialog.dispose());
        
        buttonPanel.add(saveBtn);
        buttonPanel.add(cancelBtn);
        
        gbc.gridx = 0; gbc.gridy = 6;
        gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(buttonPanel, gbc);
        
        dialog.add(panel);
        dialog.setVisible(true);
    }
    
    private JPanel createEmployeesPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        // Header
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        headerPanel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Quản Lý Nhân Viên");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerPanel.add(titleLabel, BorderLayout.WEST);
        
        JPanel buttonPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        buttonPanel.setBackground(Color.WHITE);
        
        JButton addEmployeeBtn = new JButton("+ Thêm Nhân Viên");
        addEmployeeBtn.setBackground(new Color(46, 204, 113));
        addEmployeeBtn.setForeground(Color.WHITE);
        addEmployeeBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        addEmployeeBtn.setFocusPainted(false);
        addEmployeeBtn.addActionListener(e -> showAddEmployeeDialog());
        
        buttonPanel.add(addEmployeeBtn);
        headerPanel.add(buttonPanel, BorderLayout.EAST);
        
        // Employees table
        String[] columns = {"ID", "Họ Tên", "Chức Vụ", "Email", "Điện Thoại", "Phòng Ban", "Trạng Thái"};
        employeeTableModel = new DefaultTableModel(columns, 0);
        
        JTable employeeTable = new JTable(employeeTableModel);
        employeeTable.setRowHeight(35);
        employeeTable.getTableHeader().setBackground(new Color(52, 73, 94));
        employeeTable.getTableHeader().setForeground(Color.WHITE);
        employeeTable.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        
        JScrollPane scrollPane = new JScrollPane(employeeTable);
        scrollPane.setBorder(new EmptyBorder(0, 20, 20, 20));
        
        panel.add(headerPanel, BorderLayout.NORTH);
        panel.add(scrollPane, BorderLayout.CENTER);
        
        return panel;
    }
    
    private void showAddEmployeeDialog() {
        JDialog dialog = new JDialog(this, "Thêm Nhân Viên Mới", true);
        dialog.setSize(500, 500);
        dialog.setLocationRelativeTo(this);
        
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(new EmptyBorder(20, 20, 20, 20));
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.WEST;
        
        // Form fields
        JTextField nameField = new JTextField(20);
        JTextField positionField = new JTextField(20);
        JTextField emailField = new JTextField(20);
        JTextField phoneField = new JTextField(20);
        JComboBox<String> departmentCombo = new JComboBox<>(new String[]{"IT", "Marketing", "Tài chính", "Nhân sự", "Kinh doanh", "Vận hành"});
        JComboBox<String> statusCombo = new JComboBox<>(new String[]{"Đang làm việc", "Nghỉ phép", "Nghỉ việc"});
        
        // Add components
        gbc.gridx = 0; gbc.gridy = 0;
        panel.add(new JLabel("Họ Tên:"), gbc);
        gbc.gridx = 1;
        panel.add(nameField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 1;
        panel.add(new JLabel("Chức Vụ:"), gbc);
        gbc.gridx = 1;
        panel.add(positionField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 2;
        panel.add(new JLabel("Email:"), gbc);
        gbc.gridx = 1;
        panel.add(emailField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 3;
        panel.add(new JLabel("Điện Thoại:"), gbc);
        gbc.gridx = 1;
        panel.add(phoneField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 4;
        panel.add(new JLabel("Phòng Ban:"), gbc);
        gbc.gridx = 1;
        panel.add(departmentCombo, gbc);
        
        gbc.gridx = 0; gbc.gridy = 5;
        panel.add(new JLabel("Trạng Thái:"), gbc);
        gbc.gridx = 1;
        panel.add(statusCombo, gbc);
        
        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JButton saveBtn = new JButton("Lưu");
        JButton cancelBtn = new JButton("Hủy");
        
        saveBtn.addActionListener(e -> {
            try {
                String id = "E" + String.format("%03d", employeeIdCounter++);
                String name = nameField.getText().trim();
                String position = positionField.getText().trim();
                String email = emailField.getText().trim();
                String phone = phoneField.getText().trim();
                String department = (String) departmentCombo.getSelectedItem();
                String status = (String) statusCombo.getSelectedItem();
                
                if (name.isEmpty() || position.isEmpty() || email.isEmpty()) {
                    JOptionPane.showMessageDialog(dialog, "Vui lòng điền đầy đủ thông tin bắt buộc!", "Lỗi", JOptionPane.ERROR_MESSAGE);
                    return;
                }
                
                Employee employee = new Employee(id, name, position, email, phone, department, status);
                employees.add(employee);
                employeeTableModel.addRow(employee.toArray());
                
                dialog.dispose();
                JOptionPane.showMessageDialog(this, "Thêm nhân viên thành công!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
                
                refreshHomePanel();
                
            } catch (Exception ex) {
                JOptionPane.showMessageDialog(dialog, "Có lỗi xảy ra: " + ex.getMessage(), "Lỗi", JOptionPane.ERROR_MESSAGE);
            }
        });
        
        cancelBtn.addActionListener(e -> dialog.dispose());
        
        buttonPanel.add(saveBtn);
        buttonPanel.add(cancelBtn);
        
        gbc.gridx = 0; gbc.gridy = 6;
        gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.HORIZONTAL;
        panel.add(buttonPanel, gbc);
        
        dialog.add(panel);
        dialog.setVisible(true);
    }
    
    private JPanel createReportsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        headerPanel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Báo Cáo Hệ Thống");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerPanel.add(titleLabel, BorderLayout.WEST);
        
        // Report content
        JPanel contentPanel = new JPanel(new GridLayout(2, 2, 20, 20));
        contentPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        contentPanel.setBackground(Color.WHITE);
        
        // Project Status Report
        JPanel projectReportPanel = new JPanel(new BorderLayout());
        projectReportPanel.setBorder(BorderFactory.createTitledBorder("Báo Cáo Trạng Thái Dự Án"));
        projectReportPanel.setBackground(Color.WHITE);
        
        JTextArea projectReport = new JTextArea();
        projectReport.setEditable(false);
        projectReport.setBackground(new Color(248, 249, 250));
        projectReport.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        StringBuilder projectReportText = new StringBuilder();
        projectReportText.append("TỔNG QUAN DỰ ÁN:\n");
        projectReportText.append("- Tổng số dự án: ").append(projects.size()).append("\n");
        
        int newProjects = 0, inProgressProjects = 0, pausedProjects = 0, completedProjects = 0;
        for (Project p : projects) {
            switch (p.status) {
                case "Mới tạo": newProjects++; break;
                case "Đang thực hiện": inProgressProjects++; break;
                case "Tạm dừng": pausedProjects++; break;
                case "Hoàn thành": completedProjects++; break;
            }
        }
        
        projectReportText.append("- Dự án mới: ").append(newProjects).append("\n");
        projectReportText.append("- Đang thực hiện: ").append(inProgressProjects).append("\n");
        projectReportText.append("- Tạm dừng: ").append(pausedProjects).append("\n");
        projectReportText.append("- Hoàn thành: ").append(completedProjects).append("\n");
        
        projectReport.setText(projectReportText.toString());
        projectReportPanel.add(new JScrollPane(projectReport), BorderLayout.CENTER);
        
        // Task Status Report
        JPanel taskReportPanel = new JPanel(new BorderLayout());
        taskReportPanel.setBorder(BorderFactory.createTitledBorder("Báo Cáo Công Việc"));
        taskReportPanel.setBackground(Color.WHITE);
        
        JTextArea taskReport = new JTextArea();
        taskReport.setEditable(false);
        taskReport.setBackground(new Color(248, 249, 250));
        taskReport.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        StringBuilder taskReportText = new StringBuilder();
        taskReportText.append("TỔNG QUAN CÔNG VIỆC:\n");
        taskReportText.append("- Tổng số công việc: ").append(tasks.size()).append("\n");
        
        int notStartedTasks = 0, inProgressTasks = 0, completedTasks = 0;
        for (Task t : tasks) {
            switch (t.status) {
                case "Chưa bắt đầu": notStartedTasks++; break;
                case "Đang thực hiện": inProgressTasks++; break;
                case "Hoàn thành": completedTasks++; break;
            }
        }
        
        taskReportText.append("- Chưa bắt đầu: ").append(notStartedTasks).append("\n");
        taskReportText.append("- Đang thực hiện: ").append(inProgressTasks).append("\n");
        taskReportText.append("- Hoàn thành: ").append(completedTasks).append("\n");
        
        taskReport.setText(taskReportText.toString());
        taskReportPanel.add(new JScrollPane(taskReport), BorderLayout.CENTER);
        
        // Employee Report
        JPanel employeeReportPanel = new JPanel(new BorderLayout());
        employeeReportPanel.setBorder(BorderFactory.createTitledBorder("Báo Cáo Nhân Viên"));
        employeeReportPanel.setBackground(Color.WHITE);
        
        JTextArea employeeReport = new JTextArea();
        employeeReport.setEditable(false);
        employeeReport.setBackground(new Color(248, 249, 250));
        employeeReport.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        StringBuilder employeeReportText = new StringBuilder();
        employeeReportText.append("TỔNG QUAN NHÂN VIÊN:\n");
        employeeReportText.append("- Tổng số nhân viên: ").append(employees.size()).append("\n");
        
        int activeEmployees = 0, onLeaveEmployees = 0, inactiveEmployees = 0;
        for (Employee emp : employees) {
            switch (emp.status) {
                case "Đang làm việc": activeEmployees++; break;
                case "Nghỉ phép": onLeaveEmployees++; break;
                case "Nghỉ việc": inactiveEmployees++; break;
            }
        }
        
        employeeReportText.append("- Đang làm việc: ").append(activeEmployees).append("\n");
        employeeReportText.append("- Nghỉ phép: ").append(onLeaveEmployees).append("\n");
        employeeReportText.append("- Nghỉ việc: ").append(inactiveEmployees).append("\n");
        
        employeeReport.setText(employeeReportText.toString());
        employeeReportPanel.add(new JScrollPane(employeeReport), BorderLayout.CENTER);
        
        // Export Button Panel
        JPanel exportPanel = new JPanel(new FlowLayout());
        exportPanel.setBackground(Color.WHITE);
        
        JButton exportBtn = new JButton("📄 Xuất Báo Cáo");
        exportBtn.setBackground(new Color(52, 152, 219));
        exportBtn.setForeground(Color.WHITE);
        exportBtn.setBorder(new EmptyBorder(10, 20, 10, 20));
        exportBtn.setFocusPainted(false);
        exportBtn.addActionListener(e -> {
            JOptionPane.showMessageDialog(this, "Chức năng xuất báo cáo sẽ được phát triển trong phiên bản tiếp theo!", 
                                        "Thông báo", JOptionPane.INFORMATION_MESSAGE);
        });
        
        exportPanel.add(exportBtn);
        
        contentPanel.add(projectReportPanel);
        contentPanel.add(taskReportPanel);
        contentPanel.add(employeeReportPanel);
        contentPanel.add(exportPanel);
        
        panel.add(headerPanel, BorderLayout.NORTH);
        panel.add(contentPanel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createStatisticsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        headerPanel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Thống Kê Hệ Thống");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerPanel.add(titleLabel, BorderLayout.WEST);
        
        // Statistics content
        JPanel statsPanel = new JPanel(new GridLayout(3, 1, 0, 20));
        statsPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        statsPanel.setBackground(Color.WHITE);
        
        // Project Statistics
        JPanel projectStatsPanel = new JPanel(new BorderLayout());
        projectStatsPanel.setBorder(BorderFactory.createTitledBorder("Thống Kê Dự Án"));
        projectStatsPanel.setBackground(Color.WHITE);
        
        JPanel projectStatsGrid = new JPanel(new GridLayout(2, 2, 10, 10));
        projectStatsGrid.setBackground(Color.WHITE);
        projectStatsGrid.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        // Calculate project completion rate
        int totalProjects = projects.size();
        int completedProjects = 0;
        for (Project p : projects) {
            if ("Hoàn thành".equals(p.status)) {
                completedProjects++;
            }
        }
        double completionRate = totalProjects > 0 ? (double) completedProjects / totalProjects * 100 : 0;
        
        projectStatsGrid.add(createStatLabel("Tổng dự án:", String.valueOf(totalProjects)));
        projectStatsGrid.add(createStatLabel("Đã hoàn thành:", String.valueOf(completedProjects)));
        projectStatsGrid.add(createStatLabel("Tỷ lệ hoàn thành:", String.format("%.1f%%", completionRate)));
        projectStatsGrid.add(createStatLabel("Đang thực hiện:", String.valueOf(totalProjects - completedProjects)));
        
        projectStatsPanel.add(projectStatsGrid, BorderLayout.CENTER);
        
        // Task Statistics
        JPanel taskStatsPanel = new JPanel(new BorderLayout());
        taskStatsPanel.setBorder(BorderFactory.createTitledBorder("Thống Kê Công Việc"));
        taskStatsPanel.setBackground(Color.WHITE);
        
        JPanel taskStatsGrid = new JPanel(new GridLayout(2, 2, 10, 10));
        taskStatsGrid.setBackground(Color.WHITE);
        taskStatsGrid.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        int totalTasks = tasks.size();
        int completedTasks = 0;
        int overdueTasks = 0;
        
        SimpleDateFormat sdf = new SimpleDateFormat("dd/MM/yyyy");
        Date today = new Date();
        
        for (Task t : tasks) {
            if ("Hoàn thành".equals(t.status)) {
                completedTasks++;
            }
            try {
                Date dueDate = sdf.parse(t.dueDate);
                if (dueDate.before(today) && !"Hoàn thành".equals(t.status)) {
                    overdueTasks++;
                }
            } catch (Exception e) {
                // Ignore parsing error
            }
        }
        
        taskStatsGrid.add(createStatLabel("Tổng công việc:", String.valueOf(totalTasks)));
        taskStatsGrid.add(createStatLabel("Đã hoàn thành:", String.valueOf(completedTasks)));
        taskStatsGrid.add(createStatLabel("Quá hạn:", String.valueOf(overdueTasks)));
        taskStatsGrid.add(createStatLabel("Đang thực hiện:", String.valueOf(totalTasks - completedTasks)));
        
        taskStatsPanel.add(taskStatsGrid, BorderLayout.CENTER);
        
        // Employee Statistics
        JPanel employeeStatsPanel = new JPanel(new BorderLayout());
        employeeStatsPanel.setBorder(BorderFactory.createTitledBorder("Thống Kê Nhân Viên"));
        employeeStatsPanel.setBackground(Color.WHITE);
        
        JPanel employeeStatsGrid = new JPanel(new GridLayout(2, 2, 10, 10));
        employeeStatsGrid.setBackground(Color.WHITE);
        employeeStatsGrid.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        int totalEmployees = employees.size();
        int activeEmployees = 0;
        for (Employee emp : employees) {
            if ("Đang làm việc".equals(emp.status)) {
                activeEmployees++;
            }
        }
        
        employeeStatsGrid.add(createStatLabel("Tổng nhân viên:", String.valueOf(totalEmployees)));
        employeeStatsGrid.add(createStatLabel("Đang làm việc:", String.valueOf(activeEmployees)));
        employeeStatsGrid.add(createStatLabel("Tỷ lệ hoạt động:", totalEmployees > 0 ? 
                                            String.format("%.1f%%", (double) activeEmployees / totalEmployees * 100) : "0%"));
        employeeStatsGrid.add(createStatLabel("Nghỉ/Không hoạt động:", String.valueOf(totalEmployees - activeEmployees)));
        
        employeeStatsPanel.add(employeeStatsGrid, BorderLayout.CENTER);
        
        statsPanel.add(projectStatsPanel);
        statsPanel.add(taskStatsPanel);
        statsPanel.add(employeeStatsPanel);
        
        panel.add(headerPanel, BorderLayout.NORTH);
        panel.add(statsPanel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createStatLabel(String label, String value) {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        JLabel labelComponent = new JLabel(label);
        labelComponent.setFont(new Font("Arial", Font.PLAIN, 12));
        
        JLabel valueComponent = new JLabel(value);
        valueComponent.setFont(new Font("Arial", Font.BOLD, 14));
        valueComponent.setForeground(new Color(52, 152, 219));
        
        panel.add(labelComponent, BorderLayout.WEST);
        panel.add(valueComponent, BorderLayout.EAST);
        
        return panel;
    }
    
    private JPanel createSettingsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        headerPanel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Cài Đặt Hệ Thống");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 20));
        headerPanel.add(titleLabel, BorderLayout.WEST);
        
        // Settings content
        JPanel settingsPanel = new JPanel();
        settingsPanel.setLayout(new BoxLayout(settingsPanel, BoxLayout.Y_AXIS));
        settingsPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        settingsPanel.setBackground(Color.WHITE);
        
        // User Settings
        JPanel userSettingsPanel = new JPanel(new BorderLayout());
        userSettingsPanel.setBorder(BorderFactory.createTitledBorder("Thông Tin Người Dùng"));
        userSettingsPanel.setBackground(Color.WHITE);
        userSettingsPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 150));
        
        JPanel userForm = new JPanel(new GridBagLayout());
        userForm.setBackground(Color.WHITE);
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 10, 5, 10);
        gbc.anchor = GridBagConstraints.WEST;
        
        gbc.gridx = 0; gbc.gridy = 0;
        userForm.add(new JLabel("Tên người dùng:"), gbc);
        gbc.gridx = 1;
        JTextField usernameField = new JTextField(currentUser, 15);
        usernameField.setEditable(false);
        userForm.add(usernameField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 1;
        userForm.add(new JLabel("Vai trò:"), gbc);
        gbc.gridx = 1;
        JTextField roleField = new JTextField("Quản trị viên", 15);
        roleField.setEditable(false);
        userForm.add(roleField, gbc);
        
        userSettingsPanel.add(userForm, BorderLayout.CENTER);
        
        // System Settings
        JPanel systemSettingsPanel = new JPanel(new BorderLayout());
        systemSettingsPanel.setBorder(BorderFactory.createTitledBorder("Cài Đặt Hệ Thống"));
        systemSettingsPanel.setBackground(Color.WHITE);
        systemSettingsPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 200));
        
        JPanel systemForm = new JPanel(new GridBagLayout());
        systemForm.setBackground(Color.WHITE);
        
        gbc.gridx = 0; gbc.gridy = 0;
        systemForm.add(new JLabel("Ngôn ngữ:"), gbc);
        gbc.gridx = 1;
        JComboBox<String> languageCombo = new JComboBox<>(new String[]{"Tiếng Việt", "English"});
        systemForm.add(languageCombo, gbc);
        
        gbc.gridx = 0; gbc.gridy = 1;
        systemForm.add(new JLabel("Giao diện:"), gbc);
        gbc.gridx = 1;
        JComboBox<String> themeCombo = new JComboBox<>(new String[]{"Sáng", "Tối"});
        systemForm.add(themeCombo, gbc);
        
        gbc.gridx = 0; gbc.gridy = 2;
        systemForm.add(new JLabel("Tự động lưu:"), gbc);
        gbc.gridx = 1;
        JCheckBox autoSaveCheck = new JCheckBox("Bật tự động lưu");
        autoSaveCheck.setBackground(Color.WHITE);
        autoSaveCheck.setSelected(true);
        systemForm.add(autoSaveCheck, gbc);
        
        systemSettingsPanel.add(systemForm, BorderLayout.CENTER);
        
        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(Color.WHITE);
        buttonPanel.setMaximumSize(new Dimension(Integer.MAX_VALUE, 60));
        
        JButton saveSettingsBtn = new JButton("💾 Lưu Cài Đặt");
        saveSettingsBtn.setBackground(new Color(46, 204, 113));
        saveSettingsBtn.setForeground(Color.WHITE);
        saveSettingsBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        saveSettingsBtn.setFocusPainted(false);
        saveSettingsBtn.addActionListener(e -> {
            JOptionPane.showMessageDialog(this, "Cài đặt đã được lưu thành công!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
        });
        
        JButton resetBtn = new JButton("🔄 Khôi Phục Mặc Định");
        resetBtn.setBackground(new Color(52, 152, 219));
        resetBtn.setForeground(Color.WHITE);
        resetBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        resetBtn.setFocusPainted(false);
        resetBtn.addActionListener(e -> {
            int result = JOptionPane.showConfirmDialog(this, 
                "Bạn có chắc chắn muốn khôi phục cài đặt mặc định?", 
                "Xác nhận", JOptionPane.YES_NO_OPTION);
            if (result == JOptionPane.YES_OPTION) {
                languageCombo.setSelectedIndex(0);
                themeCombo.setSelectedIndex(0);
                autoSaveCheck.setSelected(true);
                JOptionPane.showMessageDialog(this, "Đã khôi phục cài đặt mặc định!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
            }
        });
        
        buttonPanel.add(saveSettingsBtn);
        buttonPanel.add(resetBtn);
        
        settingsPanel.add(userSettingsPanel);
        settingsPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        settingsPanel.add(systemSettingsPanel);
        settingsPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        settingsPanel.add(buttonPanel);
        settingsPanel.add(Box.createVerticalGlue());
        
        panel.add(headerPanel, BorderLayout.NORTH);
        panel.add(settingsPanel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private void refreshHomePanel() {
        // Remove and recreate home panel to refresh statistics
        contentPanel.remove(contentPanel.getComponent(0));
        contentPanel.add(createHomePanel(), "HOME", 0);
        if (contentLayout.toString().contains("HOME")) {
            contentLayout.show(contentPanel, "HOME");
        }
    }
    
    private void setupLayout() {
        setLayout(new BorderLayout());
        add(sidebarPanel, BorderLayout.WEST);
        add(contentPanel, BorderLayout.CENTER);
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeel());
            } catch (Exception e) {
                e.printStackTrace();
            }
            new MainDashboard();
        });
    }
}
