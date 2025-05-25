import javax.swing.*;
import javax.swing.border.EmptyBorder;
import javax.swing.table.DefaultTableModel;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.ArrayList;
import java.util.Date;

// Main Dashboard Panel
public class MainDashboard extends JFrame {
    private JPanel sidebarPanel;
    private JPanel contentPanel;
    private CardLayout contentLayout;
    private JLabel userLabel;
    private String currentUser = "Admin"; // Replace with actual logged-in user
    
    public MainDashboard() {
        initializeComponents();
        setupLayout();
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setExtendedState(JFrame.MAXIMIZED_BOTH);
        setTitle("Hệ Thống Quản Lý Dự Án");
        setVisible(true);
    }
    
    private void initializeComponents() {
        // Create main panels
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
        // Reset all buttons
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
        
        // Add different panels
        contentPanel.add(createHomePanel(), "HOME");
        contentPanel.add(createProjectsPanel(), "PROJECTS");
        contentPanel.add(createTasksPanel(), "TASKS");
        contentPanel.add(createEmployeesPanel(), "EMPLOYEES");
        contentPanel.add(createReportsPanel(), "REPORTS");
        contentPanel.add(createStatisticsPanel(), "STATISTICS");
        contentPanel.add(createSettingsPanel(), "SETTINGS");
        
        // Show home panel by default
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
        
        JLabel dateLabel = new JLabel(new Date().toString());
        dateLabel.setFont(new Font("Arial", Font.PLAIN, 14));
        dateLabel.setForeground(Color.GRAY);
        headerPanel.add(dateLabel, BorderLayout.EAST);
        
        // Statistics cards
        JPanel statsPanel = new JPanel(new GridLayout(1, 4, 20, 0));
        statsPanel.setBorder(new EmptyBorder(30, 30, 30, 30));
        statsPanel.setBackground(Color.WHITE);
        
        statsPanel.add(createStatCard("📋 Tổng Dự Án", "15", new Color(52, 152, 219)));
        statsPanel.add(createStatCard("✅ Công Việc", "87", new Color(46, 204, 113)));
        statsPanel.add(createStatCard("👥 Nhân Viên", "23", new Color(155, 89, 182)));
        statsPanel.add(createStatCard("⏰ Đến Hạn", "5", new Color(231, 76, 60)));
        
        // Recent activities
        JPanel recentPanel = new JPanel(new BorderLayout());
        recentPanel.setBorder(BorderFactory.createTitledBorder("Hoạt Động Gần Đây"));
        recentPanel.setBackground(Color.WHITE);
        
        String[] columns = {"Thời Gian", "Người Dùng", "Hoạt Động", "Dự Án"};
        Object[][] data = {
            {"10:30", "Nguyễn Văn A", "Hoàn thành công việc", "Website ABC"},
            {"09:15", "Trần Thị B", "Tạo công việc mới", "App Mobile"},
            {"08:45", "Lê Văn C", "Cập nhật tiến độ", "Hệ thống CRM"},
            {"08:20", "Phạm Thị D", "Bình luận", "Website ABC"}
        };
        
        JTable recentTable = new JTable(data, columns);
        recentTable.setRowHeight(30);
        recentTable.getTableHeader().setBackground(new Color(52, 73, 94));
        recentTable.getTableHeader().setForeground(Color.WHITE);
        
        JScrollPane scrollPane = new JScrollPane(recentTable);
        scrollPane.setBorder(new EmptyBorder(10, 10, 10, 10));
        recentPanel.add(scrollPane, BorderLayout.CENTER);
        
        // Layout
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
        Object[][] data = {
            {"P001", "Website Bán Hàng", "Công ty ABC", "01/03/2024", "30/06/2024", "Đang thực hiện", "65%"},
            {"P002", "App Mobile Banking", "Ngân hàng XYZ", "15/02/2024", "15/08/2024", "Đang thực hiện", "40%"},
            {"P003", "Hệ thống CRM", "Tập đoàn DEF", "01/01/2024", "31/05/2024", "Hoàn thành", "100%"},
            {"P004", "Website Tin Tức", "Báo GHI", "20/03/2024", "20/07/2024", "Đang thực hiện", "25%"},
            {"P005", "Ứng dụng Giao Hàng", "Startup KLM", "10/04/2024", "10/09/2024", "Mới tạo", "5%"}
        };
        
        JTable projectTable = new JTable(data, columns);
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
        
        // Filter panel
        JPanel filterPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        filterPanel.setBackground(Color.WHITE);
        
        JComboBox<String> statusFilter = new JComboBox<>(new String[]{"Tất cả", "Chưa bắt đầu", "Đang thực hiện", "Hoàn thành"});
        JComboBox<String> priorityFilter = new JComboBox<>(new String[]{"Tất cả", "Thấp", "Trung bình", "Cao", "Rất cao"});
        
        filterPanel.add(new JLabel("Trạng thái:"));
        filterPanel.add(statusFilter);
        filterPanel.add(new JLabel("Độ ưu tiên:"));
        filterPanel.add(priorityFilter);
        
        JButton addTaskBtn = new JButton("+ Thêm Công Việc");
        addTaskBtn.setBackground(new Color(46, 204, 113));
        addTaskBtn.setForeground(Color.WHITE);
        addTaskBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        addTaskBtn.setFocusPainted(false);
        filterPanel.add(addTaskBtn);
        
        headerPanel.add(filterPanel, BorderLayout.EAST);
        
        // Tasks table
        String[] columns = {"ID", "Tên Công Việc", "Dự Án", "Người Thực Hiện", "Độ Ưu Tiên", "Ngày Hết Hạn", "Trạng Thái"};
        Object[][] data = {
            {"T001", "Thiết kế giao diện", "Website ABC", "Nguyễn Văn A", "Cao", "25/05/2024", "Đang thực hiện"},
            {"T002", "Lập trình backend", "Website ABC", "Trần Văn B", "Cao", "30/05/2024", "Chưa bắt đầu"},
            {"T003", "Test chức năng", "App Mobile", "Lê Thị C", "Trung bình", "28/05/2024", "Hoàn thành"},
            {"T004", "Viết tài liệu", "Hệ thống CRM", "Phạm Văn D", "Thấp", "02/06/2024", "Đang thực hiện"},
            {"T005", "Deploy hệ thống", "Website ABC", "Hoàng Thị E", "Rất cao", "26/05/2024", "Chưa bắt đầu"}
        };
        
        JTable taskTable = new JTable(data, columns);
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
        
        buttonPanel.add(addEmployeeBtn);
        headerPanel.add(buttonPanel, BorderLayout.EAST);
        
        // Employee table
        String[] columns = {"ID", "Họ Tên", "Chức Vụ", "Email", "Số Điện Thoại", "Phòng Ban", "Trạng Thái"};
        Object[][] data = {
            {"NV001", "Nguyễn Văn A", "Team Leader", "nva@company.com", "0123456789", "IT", "Đang làm việc"},
            {"NV002", "Trần Thị B", "Developer", "ttb@company.com", "0123456790", "IT", "Đang làm việc"},
            {"NV003", "Lê Văn C", "Designer", "lvc@company.com", "0123456791", "Design", "Đang làm việc"},
            {"NV004", "Phạm Thị D", "Tester", "ptd@company.com", "0123456792", "QA", "Đang làm việc"},
            {"NV005", "Hoàng Văn E", "Project Manager", "hve@company.com", "0123456793", "PM", "Đang làm việc"}
        };
        
        JTable employeeTable = new JTable(data, columns);
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
    
    private JPanel createReportsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Báo Cáo & Thống Kê", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setBorder(new EmptyBorder(50, 0, 50, 0));
        
        JLabel contentLabel = new JLabel("Tính năng báo cáo đang được phát triển...", SwingConstants.CENTER);
        contentLabel.setFont(new Font("Arial", Font.PLAIN, 16));
        contentLabel.setForeground(Color.GRAY);
        
        panel.add(titleLabel, BorderLayout.NORTH);
        panel.add(contentLabel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createStatisticsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Thống Kê Chi Tiết", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setBorder(new EmptyBorder(50, 0, 50, 0));
        
        JLabel contentLabel = new JLabel("Biểu đồ thống kê đang được phát triển...", SwingConstants.CENTER);
        contentLabel.setFont(new Font("Arial", Font.PLAIN, 16));
        contentLabel.setForeground(Color.GRAY);
        
        panel.add(titleLabel, BorderLayout.NORTH);
        panel.add(contentLabel, BorderLayout.CENTER);
        
        return panel;
    }
    
    private JPanel createSettingsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBackground(Color.WHITE);
        
        JLabel titleLabel = new JLabel("Cài Đặt Hệ Thống", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setBorder(new EmptyBorder(50, 0, 50, 0));
        
        JLabel contentLabel = new JLabel("Trang cài đặt đang được phát triển...", SwingConstants.CENTER);
        contentLabel.setFont(new Font("Arial", Font.PLAIN, 16));
        contentLabel.setForeground(Color.GRAY);
        
        panel.add(titleLabel, BorderLayout.NORTH);
        panel.add(contentLabel, BorderLayout.CENTER);
        
        return panel;
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
