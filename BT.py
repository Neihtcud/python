import javax.swing.*;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

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
        sidebarPanel.setPreferredSize(new Dimension(280, 0));
        sidebarPanel.setBorder(BorderFactory.createMatteBorder(0, 0, 0, 1, new Color(189, 195, 199)));
        
        // Header with company logo
        JPanel headerPanel = new JPanel();
        headerPanel.setBackground(new Color(44, 62, 80));
        headerPanel.setMaximumSize(new Dimension(280, 100));
        headerPanel.setLayout(new BorderLayout());
        headerPanel.setBorder(new EmptyBorder(15, 0, 15, 0));
        
        JPanel logoPanel = new JPanel();
        logoPanel.setBackground(new Color(44, 62, 80));
        logoPanel.setLayout(new BoxLayout(logoPanel, BoxLayout.Y_AXIS));
        
        JLabel logoLabel = new JLabel("🏢");
        logoLabel.setFont(new Font("Arial", Font.BOLD, 24));
        logoLabel.setForeground(Color.WHITE);
        logoLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel titleLabel = new JLabel("QUẢN LÝ DỰ ÁN");
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 16));
        titleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        JLabel subtitleLabel = new JLabel("Project Management");
        subtitleLabel.setForeground(new Color(189, 195, 199));
        subtitleLabel.setFont(new Font("Arial", Font.PLAIN, 10));
        subtitleLabel.setAlignmentX(Component.CENTER_ALIGNMENT);
        
        logoPanel.add(logoLabel);
        logoPanel.add(titleLabel);
        logoPanel.add(subtitleLabel);
        headerPanel.add(logoPanel, BorderLayout.CENTER);
        
        // User info with avatar
        JPanel userPanel = new JPanel(new BorderLayout());
        userPanel.setBackground(new Color(39, 55, 70));
        userPanel.setMaximumSize(new Dimension(280, 60));
        userPanel.setBorder(new EmptyBorder(12, 15, 12, 15));
        
        JPanel userInfoPanel = new JPanel(new FlowLayout(FlowLayout.LEFT, 10, 0));
        userInfoPanel.setBackground(new Color(39, 55, 70));
        
        JLabel avatarLabel = new JLabel("👤");
        avatarLabel.setFont(new Font("Arial", Font.BOLD, 20));
        avatarLabel.setForeground(Color.WHITE);
        
        JPanel textPanel = new JPanel();
        textPanel.setLayout(new BoxLayout(textPanel, BoxLayout.Y_AXIS));
        textPanel.setBackground(new Color(39, 55, 70));
        
        userLabel = new JLabel(currentUser);
        userLabel.setForeground(Color.WHITE);
        userLabel.setFont(new Font("Arial", Font.BOLD, 14));
        
        JLabel roleLabel = new JLabel("Administrator");
        roleLabel.setForeground(new Color(189, 195, 199));
        roleLabel.setFont(new Font("Arial", Font.PLAIN, 11));
        
        textPanel.add(userLabel);
        textPanel.add(roleLabel);
        
        userInfoPanel.add(avatarLabel);
        userInfoPanel.add(textPanel);
        userPanel.add(userInfoPanel, BorderLayout.WEST);
        
        // Online status
        JLabel statusLabel = new JLabel("🟢");
        statusLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        userPanel.add(statusLabel, BorderLayout.EAST);
        
        // Menu items
        sidebarPanel.add(headerPanel);
        sidebarPanel.add(userPanel);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 20)));
        
        // Menu section label
        JLabel menuLabel = new JLabel("  MENU CHÍNH");
        menuLabel.setForeground(new Color(149, 165, 166));
        menuLabel.setFont(new Font("Arial", Font.BOLD, 11));
        menuLabel.setMaximumSize(new Dimension(280, 25));
        sidebarPanel.add(menuLabel);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        
        // Navigation buttons
        addMenuButton("🏠 Trang Chủ", "HOME");
        addMenuButton("📋 Quản Lý Dự Án", "PROJECTS");
        addMenuButton("✅ Công Việc", "TASKS");
        addMenuButton("👥 Nhân Viên", "EMPLOYEES");
        addMenuButton("📊 Báo Cáo", "REPORTS");
        addMenuButton("📈 Thống Kê", "STATISTICS");
        addMenuButton("⚙️ Cài Đặt", "SETTINGS");
        
        sidebarPanel.add(Box.createVerticalGlue());
        
        // System info
        JPanel systemPanel = new JPanel();
        systemPanel.setBackground(new Color(52, 73, 94));
        systemPanel.setMaximumSize(new Dimension(280, 40));
        systemPanel.setLayout(new BoxLayout(systemPanel, BoxLayout.Y_AXIS));
        
        JLabel versionLabel = new JLabel("  Version 1.0.0");
        versionLabel.setForeground(new Color(149, 165, 166));
        versionLabel.setFont(new Font("Arial", Font.PLAIN, 10));
        
        JLabel timeLabel = new JLabel("  Online: " + java.time.LocalTime.now().toString().substring(0, 5));
        timeLabel.setForeground(new Color(149, 165, 166));
        timeLabel.setFont(new Font("Arial", Font.PLAIN, 10));
        
        systemPanel.add(versionLabel);
        systemPanel.add(timeLabel);
        sidebarPanel.add(systemPanel);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 10)));
        
        // Logout button with enhanced styling
        JButton logoutBtn = new JButton("🚪 Đăng Xuất");
        logoutBtn.setBackground(new Color(231, 76, 60));
        logoutBtn.setForeground(Color.WHITE);
        logoutBtn.setBorder(new EmptyBorder(12, 20, 12, 20));
        logoutBtn.setMaximumSize(new Dimension(250, 45));
        logoutBtn.setAlignmentX(Component.CENTER_ALIGNMENT);
        logoutBtn.setFocusPainted(false);
        logoutBtn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        logoutBtn.setFont(new Font("Arial", Font.BOLD, 12));
        
        // Hover effect for logout button
        logoutBtn.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                logoutBtn.setBackground(new Color(192, 57, 43));
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                logoutBtn.setBackground(new Color(231, 76, 60));
            }
        });
        
        sidebarPanel.add(logoutBtn);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 20)));
    }
    
    private void addMenuButton(String text, String panelName) {
        String[] parts = text.split(" ", 2);
        String icon = parts[0];
        String title = parts.length > 1 ? parts[1] : "";
        
        JButton button = new JButton();
        button.setLayout(new BorderLayout());
        button.setBackground(new Color(52, 73, 94));
        button.setForeground(Color.WHITE);
        button.setBorder(new EmptyBorder(15, 20, 15, 20));
        button.setMaximumSize(new Dimension(260, 50));
        button.setAlignmentX(Component.LEFT_ALIGNMENT);
        button.setFocusPainted(false);
        button.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        
        // Icon label
        JLabel iconLabel = new JLabel(icon);
        iconLabel.setFont(new Font("Arial", Font.PLAIN, 16));
        iconLabel.setForeground(Color.WHITE);
        iconLabel.setPreferredSize(new Dimension(25, 20));
        
        // Text label
        JLabel textLabel = new JLabel(title);
        textLabel.setFont(new Font("Arial", Font.PLAIN, 13));
        textLabel.setForeground(Color.WHITE);
        textLabel.setBorder(new EmptyBorder(0, 10, 0, 0));
        
        button.add(iconLabel, BorderLayout.WEST);
        button.add(textLabel, BorderLayout.CENTER);
        
        // Enhanced hover effect
        button.addMouseListener(new java.awt.event.MouseAdapter() {
            public void mouseEntered(java.awt.event.MouseEvent evt) {
                if (!button.getBackground().equals(new Color(41, 128, 185))) {
                    button.setBackground(new Color(44, 62, 80));
                }
            }
            public void mouseExited(java.awt.event.MouseEvent evt) {
                if (!button.getBackground().equals(new Color(41, 128, 185))) {
                    button.setBackground(new Color(52, 73, 94));
                }
            }
        });
        
        button.addActionListener(e -> {
            contentLayout.show(contentPanel, panelName);
            updateSelectedButton(button);
        });
        
        sidebarPanel.add(button);
        sidebarPanel.add(Box.createRigidArea(new Dimension(0, 2)));
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
        panel.setBackground(new Color(248, 249, 250));
        
        // Enhanced header with breadcrumb and search
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(Color.WHITE);
        headerPanel.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createMatteBorder(0, 0, 1, 0, new Color(229, 229, 229)),
            new EmptyBorder(20, 30, 20, 30)
        ));
        
        JPanel leftHeaderPanel = new JPanel();
        leftHeaderPanel.setBackground(Color.WHITE);
        leftHeaderPanel.setLayout(new BoxLayout(leftHeaderPanel, BoxLayout.Y_AXIS));
        
        JLabel titleLabel = new JLabel("Dashboard");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 28));
        titleLabel.setForeground(new Color(52, 73, 94));
        
        JLabel breadcrumbLabel = new JLabel("Trang chủ > Dashboard > Tổng quan");
        breadcrumbLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        breadcrumbLabel.setForeground(Color.GRAY);
        breadcrumbLabel.setBorder(new EmptyBorder(5, 0, 0, 0));
        
        leftHeaderPanel.add(titleLabel);
        leftHeaderPanel.add(breadcrumbLabel);
        
        JPanel rightHeaderPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        rightHeaderPanel.setBackground(Color.WHITE);
        
        // Search box
        JTextField searchField = new JTextField("🔍 Tìm kiếm...", 20);
        searchField.setFont(new Font("Arial", Font.PLAIN, 12));
        searchField.setForeground(Color.GRAY);
        searchField.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(220, 220, 220)),
            new EmptyBorder(8, 12, 8, 12)
        ));
        
        // Notification button
        JButton notificationBtn = new JButton("🔔 3");
        notificationBtn.setBackground(new Color(52, 152, 219));
        notificationBtn.setForeground(Color.WHITE);
        notificationBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        notificationBtn.setFocusPainted(false);
        notificationBtn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        
        // Refresh button
        JButton refreshBtn = new JButton("🔄 Làm mới");
        refreshBtn.setBackground(new Color(46, 204, 113));
        refreshBtn.setForeground(Color.WHITE);
        refreshBtn.setBorder(new EmptyBorder(8, 15, 8, 15));
        refreshBtn.setFocusPainted(false);
        refreshBtn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        
        rightHeaderPanel.add(searchField);
        rightHeaderPanel.add(notificationBtn);
        rightHeaderPanel.add(refreshBtn);
        
        JLabel dateLabel = new JLabel("📅 Hôm nay: " + java.time.LocalDate.now().toString());
        dateLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        dateLabel.setForeground(Color.GRAY);
        
        headerPanel.add(leftHeaderPanel, BorderLayout.WEST);
        headerPanel.add(rightHeaderPanel, BorderLayout.CENTER);
        headerPanel.add(dateLabel, BorderLayout.SOUTH);
        
        // Enhanced statistics cards with animations
        JPanel statsPanel = new JPanel(new GridLayout(1, 4, 20, 0));
        statsPanel.setBorder(new EmptyBorder(30, 30, 20, 30));
        statsPanel.setBackground(new Color(248, 249, 250));
        
        statsPanel.add(createEnhancedStatCard("📋", "Tổng Dự Án", "15", "+2 tuần này", new Color(52, 152, 219)));
        statsPanel.add(createEnhancedStatCard("✅", "Công Việc", "87", "+12 hôm nay", new Color(46, 204, 113)));
        statsPanel.add(createEnhancedStatCard("👥", "Nhân Viên", "23", "Đang hoạt động", new Color(155, 89, 182)));
        statsPanel.add(createEnhancedStatCard("⏰", "Đến Hạn", "5", "Cần xử lý", new Color(231, 76, 60)));
        
        // Enhanced recent activities with better styling
        JPanel recentPanel = new JPanel(new BorderLayout());
        recentPanel.setBackground(Color.WHITE);
        recentPanel.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(229, 229, 229)),
            new EmptyBorder(20, 20, 20, 20)
        ));
        
        JPanel recentHeaderPanel = new JPanel(new BorderLayout());
        recentHeaderPanel.setBackground(Color.WHITE);
        
        JLabel recentTitleLabel = new JLabel("📈 Hoạt Động Gần Đây");
        recentTitleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        recentTitleLabel.setForeground(new Color(52, 73, 94));
        
        JButton viewAllBtn = new JButton("Xem tất cả");
        viewAllBtn.setBackground(Color.WHITE);
        viewAllBtn.setForeground(new Color(52, 152, 219));
        viewAllBtn.setBorder(BorderFactory.createLineBorder(new Color(52, 152, 219)));
        viewAllBtn.setFocusPainted(false);
        viewAllBtn.setCursor(Cursor.getPredefinedCursor(Cursor.HAND_CURSOR));
        
        recentHeaderPanel.add(recentTitleLabel, BorderLayout.WEST);
        recentHeaderPanel.add(viewAllBtn, BorderLayout.EAST);
        
        String[] columns = {"⏰ Thời Gian", "👤 Người Dùng", "📝 Hoạt Động", "📁 Dự Án", "📊 Trạng Thái"};
        Object[][] data = {
            {"10:30 AM", "Nguyễn Văn A", "Hoàn thành công việc 'Thiết kế UI'", "Website ABC", "✅ Hoàn thành"},
            {"09:15 AM", "Trần Thị B", "Tạo công việc mới 'Test API'", "App Mobile", "🆕 Mới tạo"},
            {"08:45 AM", "Lê Văn C", "Cập nhật tiến độ 85%", "Hệ thống CRM", "🔄 Đang xử lý"},
            {"08:20 AM", "Phạm Thị D", "Bình luận về bug #123", "Website ABC", "💬 Thảo luận"},
            {"07:55 AM", "Hoàng Văn E", "Upload file thiết kế", "App Mobile", "📎 Tài liệu"}
        };
        
        JTable recentTable = new JTable(data, columns);
        recentTable.setRowHeight(40);
        recentTable.setFont(new Font("Arial", Font.PLAIN, 12));
        recentTable.getTableHeader().setBackground(new Color(52, 73, 94));
        recentTable.getTableHeader().setForeground(Color.WHITE);
        recentTable.getTableHeader().setFont(new Font("Arial", Font.BOLD, 12));
        recentTable.setGridColor(new Color(240, 240, 240));
        recentTable.setSelectionBackground(new Color(235, 245, 255));
        
        JScrollPane scrollPane = new JScrollPane(recentTable);
        scrollPane.setBorder(BorderFactory.createEmptyBorder());
        scrollPane.getViewport().setBackground(Color.WHITE);
        
        recentPanel.add(recentHeaderPanel, BorderLayout.NORTH);
        recentPanel.add(Box.createRigidArea(new Dimension(0, 15)), BorderLayout.CENTER);
        
        JPanel tablePanel = new JPanel(new BorderLayout());
        tablePanel.setBackground(Color.WHITE);
        tablePanel.add(scrollPane, BorderLayout.CENTER);
        
        // Quick actions panel
        JPanel quickActionsPanel = new JPanel(new GridLayout(1, 3, 15, 0));
        quickActionsPanel.setBackground(new Color(248, 249, 250));
        quickActionsPanel.setBorder(new EmptyBorder(20, 30, 30, 30));
        
        quickActionsPanel.add(createQuickActionCard("➕ Tạo Dự Án Mới", "Bắt đầu dự án mới", new Color(46, 204, 113)));
        quickActions
