import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import javax.swing.border.EmptyBorder;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.*;
import java.util.List;

// Model Classes
class User {
    private String id;
    private String name;
    private String username;
    private String password;
    private UserRole role;
    
    public User(String id, String name, String username, String password, UserRole role) {
        this.id = id;
        this.name = name;
        this.username = username;
        this.password = password;
        this.role = role;
    }
    
    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getUsername() { return username; }
    public String getPassword() { return password; }
    public UserRole getRole() { return role; }
}

enum UserRole {
    GIAM_DOC("Giám đốc"),
    TRUONG_PHONG("Trưởng phòng"),
    PHO_PHONG("Phó phòng"),
    NHAN_VIEN("Nhân viên");
    
    private String displayName;
    
    UserRole(String displayName) {
        this.displayName = displayName;
    }
    
    public String getDisplayName() {
        return displayName;
    }
}

class Project {
    private String id;
    private String name;
    private String description;
    private LocalDateTime startDate;
    private LocalDateTime endDate;
    private String managerId;
    private List<Phase> phases;
    
    public Project(String id, String name, String description, LocalDateTime startDate, LocalDateTime endDate) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.startDate = startDate;
        this.endDate = endDate;
        this.phases = new ArrayList<>();
    }
    
    // Getters and Setters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getDescription() { return description; }
    public LocalDateTime getStartDate() { return startDate; }
    public LocalDateTime getEndDate() { return endDate; }
    public String getManagerId() { return managerId; }
    public void setManagerId(String managerId) { this.managerId = managerId; }
    public List<Phase> getPhases() { return phases; }
}

class Phase {
    private String id;
    private String name;
    private LocalDateTime startDate;
    private LocalDateTime endDate;
    private List<Task> tasks;
    
    public Phase(String id, String name, LocalDateTime startDate, LocalDateTime endDate) {
        this.id = id;
        this.name = name;
        this.startDate = startDate;
        this.endDate = endDate;
        this.tasks = new ArrayList<>();
    }
    
    // Getters
    public String getId() { return id; }
    public String getName() { return name; }
    public LocalDateTime getStartDate() { return startDate; }
    public LocalDateTime getEndDate() { return endDate; }
    public List<Task> getTasks() { return tasks; }
}

class Task {
    private String id;
    private String name;
    private String description;
    private String assignedTo;
    private LocalDateTime startDate;
    private LocalDateTime endDate;
    private TaskStatus status;
    
    public Task(String id, String name, String description, LocalDateTime startDate, LocalDateTime endDate) {
        this.id = id;
        this.name = name;
        this.description = description;
        this.startDate = startDate;
        this.endDate = endDate;
        this.status = TaskStatus.CHUA_BAT_DAU;
    }
    
    // Getters and Setters
    public String getId() { return id; }
    public String getName() { return name; }
    public String getDescription() { return description; }
    public String getAssignedTo() { return assignedTo; }
    public void setAssignedTo(String assignedTo) { this.assignedTo = assignedTo; }
    public LocalDateTime getStartDate() { return startDate; }
    public LocalDateTime getEndDate() { return endDate; }
    public TaskStatus getStatus() { return status; }
    public void setStatus(TaskStatus status) { this.status = status; }
}

enum TaskStatus {
    CHUA_BAT_DAU("Chưa bắt đầu"),
    DANG_LAM("Đang làm"),
    HOAN_THANH("Hoàn thành"),
    QUA_HAN("Quá hạn");
    
    private String displayName;
    
    TaskStatus(String displayName) {
        this.displayName = displayName;
    }
    
    public String getDisplayName() {
        return displayName;
    }
}

// Data Manager
class DataManager {
    private static DataManager instance = new DataManager();
    private List<User> users;
    private List<Project> projects;
    private User currentUser;
    
    private DataManager() {
        users = new ArrayList<>();
        projects = new ArrayList<>();
        initializeData();
    }
    
    public static DataManager getInstance() {
        return instance;
    }
    
    private void initializeData() {
        // Sample users
        users.add(new User("1", "Nguyễn Văn An", "admin", "admin", UserRole.GIAM_DOC));
        users.add(new User("2", "Trần Thị Bình", "manager1", "123", UserRole.TRUONG_PHONG));
        users.add(new User("3", "Lê Văn Cường", "deputy1", "123", UserRole.PHO_PHONG));
        users.add(new User("4", "Phạm Thị Dung", "employee1", "123", UserRole.NHAN_VIEN));
        users.add(new User("5", "Hoàng Văn Em", "employee2", "123", UserRole.NHAN_VIEN));
        
        // Sample projects
        Project project1 = new Project("P1", "Hệ thống ERP", "Phát triển hệ thống quản lý tài nguyên doanh nghiệp", 
                                     LocalDateTime.now(), LocalDateTime.now().plusMonths(6));
        project1.setManagerId("2");
        
        Phase phase1 = new Phase("PH1", "Phân tích yêu cầu", LocalDateTime.now(), LocalDateTime.now().plusWeeks(2));
        Task task1 = new Task("T1", "Thu thập yêu cầu", "Thu thập và phân tích yêu cầu từ người dùng", 
                            LocalDateTime.now(), LocalDateTime.now().plusWeeks(1));
        task1.setAssignedTo("4");
        phase1.getTasks().add(task1);
        
        project1.getPhases().add(phase1);
        projects.add(project1);
    }
    
    public User authenticate(String username, String password) {
        return users.stream()
                .filter(u -> u.getUsername().equals(username) && u.getPassword().equals(password))
                .findFirst()
                .orElse(null);
    }
    
    public boolean registerUser(String name, String username, String password, UserRole role) {
        if (users.stream().anyMatch(u -> u.getUsername().equals(username))) {
            return false; // Username already exists
        }
        users.add(new User(String.valueOf(users.size() + 1), name, username, password, role));
        return true;
    }
    
    // Getters
    public List<User> getUsers() { return users; }
    public List<Project> getProjects() { return projects; }
    public User getCurrentUser() { return currentUser; }
    public void setCurrentUser(User user) { this.currentUser = user; }
    
    public List<User> getUsersByRole(UserRole role) {
        return users.stream().filter(u -> u.getRole() == role).toList();
    }
    
    public void addProject(Project project) {
        projects.add(project);
    }
}

// Main Application
public class ProjectManagementSystem extends JFrame {
    private CardLayout cardLayout;
    private JPanel mainPanel;
    private DataManager dataManager;
    
    public ProjectManagementSystem() {
        dataManager = DataManager.getInstance();
        initializeUI();
        showLoginPanel();
    }
    
    private void initializeUI() {
        setTitle("Hệ thống Quản lý Dự án");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1200, 800);
        setLocationRelativeTo(null);
        
        cardLayout = new CardLayout();
        mainPanel = new JPanel(cardLayout);
        
        add(mainPanel);
    }
    
    private void showLoginPanel() {
        LoginPanel loginPanel = new LoginPanel(this);
        mainPanel.add(loginPanel, "LOGIN");
        cardLayout.show(mainPanel, "LOGIN");
    }
    
    public void showRegisterPanel() {
        RegisterPanel registerPanel = new RegisterPanel(this);
        mainPanel.add(registerPanel, "REGISTER");
        cardLayout.show(mainPanel, "REGISTER");
    }
    
    public void showDashboard(User user) {
        dataManager.setCurrentUser(user);
        DashboardPanel dashboard = new DashboardPanel(this, user);
        mainPanel.add(dashboard, "DASHBOARD");
        cardLayout.show(mainPanel, "DASHBOARD");
    }
    
    public void logout() {
        dataManager.setCurrentUser(null);
        mainPanel.removeAll();
        showLoginPanel();
    }
    
    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            try {
                UIManager.setLookAndFeel(UIManager.getSystemLookAndFeel());
            } catch (Exception e) {
                e.printStackTrace();
            }
            new ProjectManagementSystem().setVisible(true);
        });
    }
}

// Login Panel
class LoginPanel extends JPanel {
    private ProjectManagementSystem mainFrame;
    private JTextField usernameField;
    private JPasswordField passwordField;
    
    public LoginPanel(ProjectManagementSystem mainFrame) {
        this.mainFrame = mainFrame;
        initializeUI();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(new Color(240, 248, 255));
        
        // Header
        JPanel headerPanel = new JPanel();
        headerPanel.setBackground(new Color(70, 130, 180));
        headerPanel.setPreferredSize(new Dimension(0, 80));
        JLabel titleLabel = new JLabel("HỆ THỐNG QUẢN LÝ DỰ ÁN", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        headerPanel.add(titleLabel);
        add(headerPanel, BorderLayout.NORTH);
        
        // Login Form
        JPanel centerPanel = new JPanel(new GridBagLayout());
        centerPanel.setBackground(new Color(240, 248, 255));
        
        JPanel loginForm = new JPanel(new GridBagLayout());
        loginForm.setBackground(Color.WHITE);
        loginForm.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createRaisedBevelBorder(),
            new EmptyBorder(30, 30, 30, 30)
        ));
        loginForm.setPreferredSize(new Dimension(400, 300));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        
        // Title
        JLabel loginTitle = new JLabel("ĐĂNG NHẬP");
        loginTitle.setFont(new Font("Arial", Font.BOLD, 18));
        loginTitle.setForeground(new Color(70, 130, 180));
        gbc.gridx = 0; gbc.gridy = 0; gbc.gridwidth = 2;
        loginForm.add(loginTitle, gbc);
        
        // Username
        gbc.gridwidth = 1; gbc.gridy = 1;
        loginForm.add(new JLabel("Tên đăng nhập:"), gbc);
        gbc.gridx = 1;
        usernameField = new JTextField(15);
        usernameField.setText("admin"); // Default for testing
        loginForm.add(usernameField, gbc);
        
        // Password
        gbc.gridx = 0; gbc.gridy = 2;
        loginForm.add(new JLabel("Mật khẩu:"), gbc);
        gbc.gridx = 1;
        passwordField = new JPasswordField(15);
        passwordField.setText("admin"); // Default for testing
        loginForm.add(passwordField, gbc);
        
        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(Color.WHITE);
        
        JButton loginButton = new JButton("Đăng nhập");
        loginButton.setBackground(new Color(70, 130, 180));
        loginButton.setForeground(Color.WHITE);
        loginButton.setPreferredSize(new Dimension(100, 35));
        loginButton.addActionListener(this::loginAction);
        
        JButton registerButton = new JButton("Đăng ký");
        registerButton.setBackground(new Color(60, 179, 113));
        registerButton.setForeground(Color.WHITE);
        registerButton.setPreferredSize(new Dimension(100, 35));
        registerButton.addActionListener(e -> mainFrame.showRegisterPanel());
        
        buttonPanel.add(loginButton);
        buttonPanel.add(registerButton);
        
        gbc.gridx = 0; gbc.gridy = 3; gbc.gridwidth = 2;
        loginForm.add(buttonPanel, gbc);
        
        centerPanel.add(loginForm);
        add(centerPanel, BorderLayout.CENTER);
        
        // Sample credentials info
        JPanel infoPanel = new JPanel();
        infoPanel.setBackground(new Color(240, 248, 255));
        infoPanel.add(new JLabel("Tài khoản mẫu: admin/admin (Giám đốc), manager1/123 (Trưởng phòng), employee1/123 (Nhân viên)"));
        add(infoPanel, BorderLayout.SOUTH);
    }
    
    private void loginAction(ActionEvent e) {
        String username = usernameField.getText().trim();
        String password = new String(passwordField.getPassword());
        
        if (username.isEmpty() || password.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Vui lòng nhập đầy đủ thông tin!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        User user = DataManager.getInstance().authenticate(username, password);
        if (user != null) {
            mainFrame.showDashboard(user);
        } else {
            JOptionPane.showMessageDialog(this, "Tên đăng nhập hoặc mật khẩu không đúng!", "Lỗi", JOptionPane.ERROR_MESSAGE);
        }
    }
}

// Register Panel
class RegisterPanel extends JPanel {
    private ProjectManagementSystem mainFrame;
    private JTextField nameField, usernameField;
    private JPasswordField passwordField, confirmPasswordField;
    private JComboBox<UserRole> roleComboBox;
    
    public RegisterPanel(ProjectManagementSystem mainFrame) {
        this.mainFrame = mainFrame;
        initializeUI();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(new Color(240, 248, 255));
        
        // Header
        JPanel headerPanel = new JPanel();
        headerPanel.setBackground(new Color(70, 130, 180));
        headerPanel.setPreferredSize(new Dimension(0, 80));
        JLabel titleLabel = new JLabel("ĐĂNG KÝ TÀI KHOẢN", SwingConstants.CENTER);
        titleLabel.setFont(new Font("Arial", Font.BOLD, 24));
        titleLabel.setForeground(Color.WHITE);
        headerPanel.add(titleLabel);
        add(headerPanel, BorderLayout.NORTH);
        
        // Register Form
        JPanel centerPanel = new JPanel(new GridBagLayout());
        centerPanel.setBackground(new Color(240, 248, 255));
        
        JPanel registerForm = new JPanel(new GridBagLayout());
        registerForm.setBackground(Color.WHITE);
        registerForm.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createRaisedBevelBorder(),
            new EmptyBorder(30, 30, 30, 30)
        ));
        registerForm.setPreferredSize(new Dimension(450, 400));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        
        // Form fields
        gbc.gridx = 0; gbc.gridy = 0;
        registerForm.add(new JLabel("Họ tên:"), gbc);
        gbc.gridx = 1;
        nameField = new JTextField(15);
        registerForm.add(nameField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 1;
        registerForm.add(new JLabel("Tên đăng nhập:"), gbc);
        gbc.gridx = 1;
        usernameField = new JTextField(15);
        registerForm.add(usernameField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 2;
        registerForm.add(new JLabel("Mật khẩu:"), gbc);
        gbc.gridx = 1;
        passwordField = new JPasswordField(15);
        registerForm.add(passwordField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 3;
        registerForm.add(new JLabel("Xác nhận mật khẩu:"), gbc);
        gbc.gridx = 1;
        confirmPasswordField = new JPasswordField(15);
        registerForm.add(confirmPasswordField, gbc);
        
        gbc.gridx = 0; gbc.gridy = 4;
        registerForm.add(new JLabel("Chức vụ:"), gbc);
        gbc.gridx = 1;
        roleComboBox = new JComboBox<>(UserRole.values());
        roleComboBox.setRenderer(new DefaultListCellRenderer() {
            @Override
            public Component getListCellRendererComponent(JList<?> list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
                super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
                if (value instanceof UserRole) {
                    setText(((UserRole) value).getDisplayName());
                }
                return this;
            }
        });
        registerForm.add(roleComboBox, gbc);
        
        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(Color.WHITE);
        
        JButton registerButton = new JButton("Đăng ký");
        registerButton.setBackground(new Color(60, 179, 113));
        registerButton.setForeground(Color.WHITE);
        registerButton.setPreferredSize(new Dimension(100, 35));
        registerButton.addActionListener(this::registerAction);
        
        JButton backButton = new JButton("Quay lại");
        backButton.setBackground(new Color(169, 169, 169));
        backButton.setForeground(Color.WHITE);
        backButton.setPreferredSize(new Dimension(100, 35));
        backButton.addActionListener(e -> mainFrame.showLoginPanel());
        
        buttonPanel.add(registerButton);
        buttonPanel.add(backButton);
        
        gbc.gridx = 0; gbc.gridy = 5; gbc.gridwidth = 2;
        registerForm.add(buttonPanel, gbc);
        
        centerPanel.add(registerForm);
        add(centerPanel, BorderLayout.CENTER);
    }
    
    private void registerAction(ActionEvent e) {
        String name = nameField.getText().trim();
        String username = usernameField.getText().trim();
        String password = new String(passwordField.getPassword());
        String confirmPassword = new String(confirmPasswordField.getPassword());
        UserRole role = (UserRole) roleComboBox.getSelectedItem();
        
        if (name.isEmpty() || username.isEmpty() || password.isEmpty()) {
            JOptionPane.showMessageDialog(this, "Vui lòng nhập đầy đủ thông tin!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        if (!password.equals(confirmPassword)) {
            JOptionPane.showMessageDialog(this, "Mật khẩu xác nhận không khớp!", "Lỗi", JOptionPane.ERROR_MESSAGE);
            return;
        }
        
        if (DataManager.getInstance().registerUser(name, username, password, role)) {
            JOptionPane.showMessageDialog(this, "Đăng ký thành công!", "Thành công", JOptionPane.INFORMATION_MESSAGE);
            mainFrame.showLoginPanel();
        } else {
            JOptionPane.showMessageDialog(this, "Tên đăng nhập đã tồn tại!", "Lỗi", JOptionPane.ERROR_MESSAGE);
        }
    }
}

// Dashboard Panel
class DashboardPanel extends JPanel {
    private ProjectManagementSystem mainFrame;
    private User currentUser;
    private JPanel contentPanel;
    private CardLayout contentLayout;
    
    public DashboardPanel(ProjectManagementSystem mainFrame, User user) {
        this.mainFrame = mainFrame;
        this.currentUser = user;
        initializeUI();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        
        // Header
        JPanel headerPanel = createHeaderPanel();
        add(headerPanel, BorderLayout.NORTH);
        
        // Sidebar
        JPanel sidebarPanel = createSidebarPanel();
        add(sidebarPanel, BorderLayout.WEST);
        
        // Content
        contentLayout = new CardLayout();
        contentPanel = new JPanel(contentLayout);
        contentPanel.add(new HomePanel(currentUser), "HOME");
        contentPanel.add(new ProjectManagementPanel(currentUser), "PROJECTS");
        contentPanel.add(new TaskManagementPanel(currentUser), "TASKS");
        contentPanel.add(new UserManagementPanel(currentUser), "USERS");
        contentPanel.add(new ReportPanel(currentUser), "REPORTS");
        
        add(contentPanel, BorderLayout.CENTER);
        
        // Show home by default
        contentLayout.show(contentPanel, "HOME");
    }
    
    private JPanel createHeaderPanel() {
        JPanel headerPanel = new JPanel(new BorderLayout());
        headerPanel.setBackground(new Color(70, 130, 180));
        headerPanel.setPreferredSize(new Dimension(0, 60));
        
        JLabel titleLabel = new JLabel("HỆ THỐNG QUẢN LÝ DỰ ÁN");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setBorder(new EmptyBorder(0, 20, 0, 0));
        
        JPanel userPanel = new JPanel(new FlowLayout(FlowLayout.RIGHT));
        userPanel.setBackground(new Color(70, 130, 180));
        
        JLabel userLabel = new JLabel("Xin chào, " + currentUser.getName() + " (" + currentUser.getRole().getDisplayName() + ")");
        userLabel.setForeground(Color.WHITE);
        
        JButton logoutButton = new JButton("Đăng xuất");
        logoutButton.setBackground(new Color(220, 20, 60));
        logoutButton.setForeground(Color.WHITE);
        logoutButton.addActionListener(e -> mainFrame.logout());
        
        userPanel.add(userLabel);
        userPanel.add(Box.createHorizontalStrut(20));
        userPanel.add(logoutButton);
        
        headerPanel.add(titleLabel, BorderLayout.WEST);
        headerPanel.add(userPanel, BorderLayout.EAST);
        
        return headerPanel;
    }
    
    private JPanel createSidebarPanel() {
        JPanel sidebarPanel = new JPanel();
        sidebarPanel.setLayout(new BoxLayout(sidebarPanel, BoxLayout.Y_AXIS));
        sidebarPanel.setBackground(new Color(248, 249, 250));
        sidebarPanel.setPreferredSize(new Dimension(200, 0));
        sidebarPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        String[] menuItems = {"Trang chủ", "Quản lý dự án", "Quản lý công việc", "Quản lý nhân sự", "Báo cáo"};
        String[] cardNames = {"HOME", "PROJECTS", "TASKS", "USERS", "REPORTS"};
        
        for (int i = 0; i < menuItems.length; i++) {
            JButton menuButton = createMenuButton(menuItems[i], cardNames[i]);
            sidebarPanel.add(menuButton);
            sidebarPanel.add(Box.createVerticalStrut(5));
        }
        
        return sidebarPanel;
    }
    
    private JButton createMenuButton(String text, String cardName) {
        JButton button = new JButton(text);
        button.setAlignmentX(Component.CENTER_ALIGNMENT);
        button.setMaximumSize(new Dimension(180, 40));
        button.setBackground(Color.WHITE);
        button.setForeground(new Color(70, 130, 180));
        button.setBorder(BorderFactory.createCompoundBorder(
            BorderFactory.createLineBorder(new Color(70, 130, 180)),
            new EmptyBorder(8, 15, 8, 15)
        ));
        button.setFocusPainted(false);
        
        button.addActionListener(e -> contentLayout.show(contentPanel, cardName));
        
        return button;
    }
}

// Home Panel
class HomePanel extends JPanel {
    private User currentUser;
    
    public HomePanel(User user) {
        this.currentUser = user;
        initializeUI();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(Color.WHITE);
        
        JPanel welcomePanel = new JPanel(new GridBagLayout());
        welcomePanel.setBackground(Color.WHITE);
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(20, 20, 20, 20);
        
        JLabel welcomeLabel = new JLabel("Chào mừng đến với Hệ thống Quản lý Dự án!");
        welcomeLabel.setFont(new Font("Arial", Font.BOLD, 24));
        welcomeLabel.setForeground(new Color(70, 130, 180));
        gbc.gridx = 0; gbc.gridy = 0;
        welcomePanel.add(welcomeLabel, gbc);
        
        JLabel userInfoLabel = new JLabel("<html><center>Bạn đang đăng nhập với quyền: <b>" + 
                                        currentUser.getRole().getDisplayName() + "</b><br>" +
                                        "Tên: <b>" + currentUser.getName() + "</b></center></html>");
        userInfoLabel.setFont(new Font("Arial", Font.PLAIN, 16));
        gbc.gridy = 1;
        welcomePanel.add(userInfoLabel, gbc);
        
        // Statistics Panel
        JPanel statsPanel = createStatsPanel();
        gbc.gridy = 2;
        welcomePanel.add(statsPanel, gbc);
        
        add(welcomePanel, BorderLayout.CENTER);
    }
    
    private JPanel createStatsPanel() {
        JPanel statsPanel = new JPanel(new GridLayout(2, 2, 20, 20));
        statsPanel.setBorder(BorderFactory.createTitledBorder("Thống kê tổng quan"));
        
        DataManager dm = DataManager.getInstance();
        
        // Project count
        JPanel projectCard = createStatCard("Tổng số dự án", String.valueOf(dm.getProjects().size()), new Color(70, 130, 180));
        statsPanel.add(projectCard);
        
        // User count
        JPanel userCard = createStatCard("Tổng số nhân viên", String.valueOf(dm.getUsers().size()), new Color(60, 179, 113));
        statsPanel.add(userCard);
        
        // Active tasks
        long activeTasks = dm.getProjects().stream()
                .flatMap(p -> p.getPhases().stream())
                .flatMap(ph -> ph.getTasks().stream())
                .filter(t -> t.getStatus() == TaskStatus.DANG_LAM)
                .count();
        JPanel taskCard = createStatCard("Công việc đang thực hiện", String.valueOf(activeTasks), new Color(255, 165, 0));
        statsPanel.add(taskCard);
        
        // Overdue tasks
        long overdueTasks = dm.getProjects().stream()
                .flatMap(p -> p.getPhases().stream())
                .flatMap(ph -> ph.getTasks().stream())
                .filter(t -> t.getStatus() == TaskStatus.QUA_HAN)
                .count();
        // Tiếp tục từ phần createStatsPanel() trong HomePanel
        JPanel overdueCard = createStatCard("Công việc quá hạn", String.valueOf(overdueTasks), new Color(220, 20, 60));
        statsPanel.add(overdueCard);
        
        return statsPanel;
    }
    
    private JPanel createStatCard(String title, String value, Color color) {
        JPanel card = new JPanel(new BorderLayout());
        card.setBackground(color);
        card.setBorder(new EmptyBorder(15, 15, 15, 15));
        card.setPreferredSize(new Dimension(150, 80));
        
        JLabel titleLabel = new JLabel(title, SwingConstants.CENTER);
        titleLabel.setForeground(Color.WHITE);
        titleLabel.setFont(new Font("Arial", Font.PLAIN, 12));
        
        JLabel valueLabel = new JLabel(value, SwingConstants.CENTER);
        valueLabel.setForeground(Color.WHITE);
        valueLabel.setFont(new Font("Arial", Font.BOLD, 24));
        
        card.add(titleLabel, BorderLayout.NORTH);
        card.add(valueLabel, BorderLayout.CENTER);
        
        return card;
    }
}

// Project Management Panel
class ProjectManagementPanel extends JPanel {
    private User currentUser;
    private JTable projectTable;
    private DefaultTableModel tableModel;
    
    public ProjectManagementPanel(User user) {
        this.currentUser = user;
        initializeUI();
        loadProjects();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(Color.WHITE);
        
        // Header
        JPanel headerPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        headerPanel.setBackground(Color.WHITE);
        headerPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        JLabel titleLabel = new JLabel("Quản lý Dự án");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        titleLabel.setForeground(new Color(70, 130, 180));
        headerPanel.add(titleLabel);
        
        if (currentUser.getRole() == UserRole.GIAM_DOC || currentUser.getRole() == UserRole.TRUONG_PHONG) {
            JButton addButton = new JButton("Thêm dự án mới");
            addButton.setBackground(new Color(60, 179, 113));
            addButton.setForeground(Color.WHITE);
            addButton.addActionListener(this::addProject);
            headerPanel.add(Box.createHorizontalStrut(20));
            headerPanel.add(addButton);
        }
        
        add(headerPanel, BorderLayout.NORTH);
        
        // Table
        String[] columns = {"ID", "Tên dự án", "Mô tả", "Ngày bắt đầu", "Ngày kết thúc", "Người quản lý"};
        tableModel = new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        
        projectTable = new JTable(tableModel);
        projectTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        projectTable.getTableHeader().setBackground(new Color(70, 130, 180));
        projectTable.getTableHeader().setForeground(Color.WHITE);
        
        JScrollPane scrollPane = new JScrollPane(projectTable);
        add(scrollPane, BorderLayout.CENTER);
        
        // Button panel
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(Color.WHITE);
        
        JButton viewButton = new JButton("Xem chi tiết");
        viewButton.addActionListener(this::viewProject);
        buttonPanel.add(viewButton);
        
        if (currentUser.getRole() == UserRole.GIAM_DOC || currentUser.getRole() == UserRole.TRUONG_PHONG) {
            JButton editButton = new JButton("Chỉnh sửa");
            editButton.addActionListener(this::editProject);
            buttonPanel.add(editButton);
            
            JButton deleteButton = new JButton("Xóa");
            deleteButton.setBackground(new Color(220, 20, 60));
            deleteButton.setForeground(Color.WHITE);
            deleteButton.addActionListener(this::deleteProject);
            buttonPanel.add(deleteButton);
        }
        
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void loadProjects() {
        tableModel.setRowCount(0);
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        
        for (Project project : DataManager.getInstance().getProjects()) {
            User manager = DataManager.getInstance().getUsers().stream()
                    .filter(u -> u.getId().equals(project.getManagerId()))
                    .findFirst().orElse(null);
            
            Object[] row = {
                project.getId(),
                project.getName(),
                project.getDescription(),
                project.getStartDate().format(formatter),
                project.getEndDate().format(formatter),
                manager != null ? manager.getName() : "Chưa phân công"
            };
            tableModel.addRow(row);
        }
    }
    
    private void addProject(ActionEvent e) {
        ProjectDialog dialog = new ProjectDialog(null, "Thêm dự án mới", null);
        dialog.setVisible(true);
        if (dialog.isConfirmed()) {
            loadProjects();
        }
    }
    
    private void editProject(ActionEvent e) {
        int selectedRow = projectTable.getSelectedRow();
        if (selectedRow >= 0) {
            String projectId = (String) tableModel.getValueAt(selectedRow, 0);
            Project project = DataManager.getInstance().getProjects().stream()
                    .filter(p -> p.getId().equals(projectId))
                    .findFirst().orElse(null);
            
            if (project != null) {
                ProjectDialog dialog = new ProjectDialog(null, "Chỉnh sửa dự án", project);
                dialog.setVisible(true);
                if (dialog.isConfirmed()) {
                    loadProjects();
                }
            }
        } else {
            JOptionPane.showMessageDialog(this, "Vui lòng chọn dự án cần chỉnh sửa!");
        }
    }
    
    private void deleteProject(ActionEvent e) {
        int selectedRow = projectTable.getSelectedRow();
        if (selectedRow >= 0) {
            int result = JOptionPane.showConfirmDialog(this, 
                "Bạn có chắc chắn muốn xóa dự án này?", 
                "Xác nhận xóa", 
                JOptionPane.YES_NO_OPTION);
            
            if (result == JOptionPane.YES_OPTION) {
                String projectId = (String) tableModel.getValueAt(selectedRow, 0);
                DataManager.getInstance().getProjects().removeIf(p -> p.getId().equals(projectId));
                loadProjects();
                JOptionPane.showMessageDialog(this, "Đã xóa dự án thành công!");
            }
        } else {
            JOptionPane.showMessageDialog(this, "Vui lòng chọn dự án cần xóa!");
        }
    }
    
    private void viewProject(ActionEvent e) {
        int selectedRow = projectTable.getSelectedRow();
        if (selectedRow >= 0) {
            String projectId = (String) tableModel.getValueAt(selectedRow, 0);
            Project project = DataManager.getInstance().getProjects().stream()
                    .filter(p -> p.getId().equals(projectId))
                    .findFirst().orElse(null);
            
            if (project != null) {
                ProjectDetailDialog dialog = new ProjectDetailDialog(null, project);
                dialog.setVisible(true);
            }
        } else {
            JOptionPane.showMessageDialog(this, "Vui lòng chọn dự án cần xem!");
        }
    }
}

// Project Dialog
class ProjectDialog extends JDialog {
    private JTextField nameField, descriptionField;
    private JTextField startDateField, endDateField;
    private JComboBox<User> managerComboBox;
    private boolean confirmed = false;
    private Project project;
    
    public ProjectDialog(Frame parent, String title, Project project) {
        super(parent, title, true);
        this.project = project;
        initializeUI();
        if (project != null) {
            populateFields();
        }
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setSize(500, 400);
        setLocationRelativeTo(getParent());
        
        JPanel formPanel = new JPanel(new GridBagLayout());
        formPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 5, 5, 5);
        gbc.anchor = GridBagConstraints.WEST;
        
        // Name
        gbc.gridx = 0; gbc.gridy = 0;
        formPanel.add(new JLabel("Tên dự án:"), gbc);
        gbc.gridx = 1; gbc.fill = GridBagConstraints.HORIZONTAL;
        nameField = new JTextField(20);
        formPanel.add(nameField, gbc);
        
        // Description
        gbc.gridx = 0; gbc.gridy = 1; gbc.fill = GridBagConstraints.NONE;
        formPanel.add(new JLabel("Mô tả:"), gbc);
        gbc.gridx = 1; gbc.fill = GridBagConstraints.HORIZONTAL;
        descriptionField = new JTextField(20);
        formPanel.add(descriptionField, gbc);
        
        // Start Date
        gbc.gridx = 0; gbc.gridy = 2; gbc.fill = GridBagConstraints.NONE;
        formPanel.add(new JLabel("Ngày bắt đầu (dd/MM/yyyy):"), gbc);
        gbc.gridx = 1; gbc.fill = GridBagConstraints.HORIZONTAL;
        startDateField = new JTextField(20);
        formPanel.add(startDateField, gbc);
        
        // End Date
        gbc.gridx = 0; gbc.gridy = 3; gbc.fill = GridBagConstraints.NONE;
        formPanel.add(new JLabel("Ngày kết thúc (dd/MM/yyyy):"), gbc);
        gbc.gridx = 1; gbc.fill = GridBagConstraints.HORIZONTAL;
        endDateField = new JTextField(20);
        formPanel.add(endDateField, gbc);
        
        // Manager
        gbc.gridx = 0; gbc.gridy = 4; gbc.fill = GridBagConstraints.NONE;
        formPanel.add(new JLabel("Người quản lý:"), gbc);
        gbc.gridx = 1; gbc.fill = GridBagConstraints.HORIZONTAL;
        
        List<User> managers = DataManager.getInstance().getUsersByRole(UserRole.TRUONG_PHONG);
        managers.addAll(DataManager.getInstance().getUsersByRole(UserRole.GIAM_DOC));
        managerComboBox = new JComboBox<>(managers.toArray(new User[0]));
        managerComboBox.setRenderer(new DefaultListCellRenderer() {
            @Override
            public Component getListCellRendererComponent(JList<?> list, Object value, int index, boolean isSelected, boolean cellHasFocus) {
                super.getListCellRendererComponent(list, value, index, isSelected, cellHasFocus);
                if (value instanceof User) {
                    setText(((User) value).getName() + " (" + ((User) value).getRole().getDisplayName() + ")");
                }
                return this;
            }
        });
        formPanel.add(managerComboBox, gbc);
        
        add(formPanel, BorderLayout.CENTER);
        
        // Buttons
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JButton saveButton = new JButton("Lưu");
        saveButton.setBackground(new Color(60, 179, 113));
        saveButton.setForeground(Color.WHITE);
        saveButton.addActionListener(this::saveProject);
        
        JButton cancelButton = new JButton("Hủy");
        cancelButton.addActionListener(e -> dispose());
        
        buttonPanel.add(saveButton);
        buttonPanel.add(cancelButton);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void populateFields() {
        nameField.setText(project.getName());
        descriptionField.setText(project.getDescription());
        
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        startDateField.setText(project.getStartDate().format(formatter));
        endDateField.setText(project.getEndDate().format(formatter));
        
        // Set manager
        if (project.getManagerId() != null) {
            User manager = DataManager.getInstance().getUsers().stream()
                    .filter(u -> u.getId().equals(project.getManagerId()))
                    .findFirst().orElse(null);
            if (manager != null) {
                managerComboBox.setSelectedItem(manager);
            }
        }
    }
    
    private void saveProject(ActionEvent e) {
        try {
            String name = nameField.getText().trim();
            String description = descriptionField.getText().trim();
            
            if (name.isEmpty()) {
                JOptionPane.showMessageDialog(this, "Vui lòng nhập tên dự án!");
                return;
            }
            
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
            LocalDateTime startDate = LocalDateTime.parse(startDateField.getText().trim() + " 00:00", 
                    DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm"));
            LocalDateTime endDate = LocalDateTime.parse(endDateField.getText().trim() + " 23:59", 
                    DateTimeFormatter.ofPattern("dd/MM/yyyy HH:mm"));
            
            User selectedManager = (User) managerComboBox.getSelectedItem();
            
            if (project == null) {
                // Add new project
                String newId = "P" + (DataManager.getInstance().getProjects().size() + 1);
                Project newProject = new Project(newId, name, description, startDate, endDate);
                if (selectedManager != null) {
                    newProject.setManagerId(selectedManager.getId());
                }
                DataManager.getInstance().addProject(newProject);
            } else {
                // Update existing project - In a real application, you'd have setters for these fields
                JOptionPane.showMessageDialog(this, "Chức năng chỉnh sửa sẽ được cập nhật trong phiên bản sau!");
            }
            
            confirmed = true;
            dispose();
            
        } catch (Exception ex) {
            JOptionPane.showMessageDialog(this, "Định dạng ngày không hợp lệ! Vui lòng sử dụng định dạng dd/MM/yyyy");
        }
    }
    
    public boolean isConfirmed() {
        return confirmed;
    }
}

// Project Detail Dialog
class ProjectDetailDialog extends JDialog {
    private Project project;
    
    public ProjectDetailDialog(Frame parent, Project project) {
        super(parent, "Chi tiết dự án: " + project.getName(), true);
        this.project = project;
        initializeUI();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setSize(600, 500);
        setLocationRelativeTo(getParent());
        
        JTabbedPane tabbedPane = new JTabbedPane();
        
        // Project Info Tab
        JPanel infoPanel = createProjectInfoPanel();
        tabbedPane.addTab("Thông tin dự án", infoPanel);
        
        // Phases Tab
        JPanel phasesPanel = createPhasesPanel();
        tabbedPane.addTab("Các giai đoạn", phasesPanel);
        
        add(tabbedPane, BorderLayout.CENTER);
        
        // Close button
        JPanel buttonPanel = new JPanel(new FlowLayout());
        JButton closeButton = new JButton("Đóng");
        closeButton.addActionListener(e -> dispose());
        buttonPanel.add(closeButton);
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private JPanel createProjectInfoPanel() {
        JPanel panel = new JPanel(new GridBagLayout());
        panel.setBorder(new EmptyBorder(20, 20, 20, 20));
        
        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.anchor = GridBagConstraints.WEST;
        
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        
        // Project details
        gbc.gridx = 0; gbc.gridy = 0;
        panel.add(new JLabel("ID:"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel(project.getId()), gbc);
        
        gbc.gridx = 0; gbc.gridy = 1;
        panel.add(new JLabel("Tên dự án:"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel(project.getName()), gbc);
        
        gbc.gridx = 0; gbc.gridy = 2;
        panel.add(new JLabel("Mô tả:"), gbc);
        gbc.gridx = 1;
        JTextArea descArea = new JTextArea(project.getDescription());
        descArea.setEditable(false);
        descArea.setBackground(panel.getBackground());
        panel.add(descArea, gbc);
        
        gbc.gridx = 0; gbc.gridy = 3;
        panel.add(new JLabel("Ngày bắt đầu:"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel(project.getStartDate().format(formatter)), gbc);
        
        gbc.gridx = 0; gbc.gridy = 4;
        panel.add(new JLabel("Ngày kết thúc:"), gbc);
        gbc.gridx = 1;
        panel.add(new JLabel(project.getEndDate().format(formatter)), gbc);
        
        gbc.gridx = 0; gbc.gridy = 5;
        panel.add(new JLabel("Người quản lý:"), gbc);
        gbc.gridx = 1;
        User manager = DataManager.getInstance().getUsers().stream()
                .filter(u -> u.getId().equals(project.getManagerId()))
                .findFirst().orElse(null);
        panel.add(new JLabel(manager != null ? manager.getName() : "Chưa phân công"), gbc);
        
        return panel;
    }
    
    private JPanel createPhasesPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        
        if (project.getPhases().isEmpty()) {
            JLabel noDataLabel = new JLabel("Chưa có giai đoạn nào được tạo", SwingConstants.CENTER);
            panel.add(noDataLabel, BorderLayout.CENTER);
        } else {
            String[] columns = {"ID", "Tên giai đoạn", "Ngày bắt đầu", "Ngày kết thúc", "Số công việc"};
            DefaultTableModel model = new DefaultTableModel(columns, 0);
            
            DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
            for (Phase phase : project.getPhases()) {
                Object[] row = {
                    phase.getId(),
                    phase.getName(),
                    phase.getStartDate().format(formatter),
                    phase.getEndDate().format(formatter),
                    phase.getTasks().size()
                };
                model.addRow(row);
            }
            
            JTable table = new JTable(model);
            table.getTableHeader().setBackground(new Color(70, 130, 180));
            table.getTableHeader().setForeground(Color.WHITE);
            
            JScrollPane scrollPane = new JScrollPane(table);
            panel.add(scrollPane, BorderLayout.CENTER);
        }
        
        return panel;
    }
}

// Task Management Panel
class TaskManagementPanel extends JPanel {
    private User currentUser;
    private JTable taskTable;
    private DefaultTableModel tableModel;
    
    public TaskManagementPanel(User user) {
        this.currentUser = user;
        initializeUI();
        loadTasks();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(Color.WHITE);
        
        // Header
        JPanel headerPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        headerPanel.setBackground(Color.WHITE);
        headerPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        JLabel titleLabel = new JLabel("Quản lý Công việc");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        titleLabel.setForeground(new Color(70, 130, 180));
        headerPanel.add(titleLabel);
        
        add(headerPanel, BorderLayout.NORTH);
        
        // Table
        String[] columns = {"ID", "Tên công việc", "Mô tả", "Người thực hiện", "Ngày bắt đầu", "Ngày kết thúc", "Trạng thái"};
        tableModel = new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        
        taskTable = new JTable(tableModel);
        taskTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        taskTable.getTableHeader().setBackground(new Color(70, 130, 180));
        taskTable.getTableHeader().setForeground(Color.WHITE);
        
        JScrollPane scrollPane = new JScrollPane(taskTable);
        add(scrollPane, BorderLayout.CENTER);
        
        // Button panel
        JPanel buttonPanel = new JPanel(new FlowLayout());
        buttonPanel.setBackground(Color.WHITE);
        
        JButton updateStatusButton = new JButton("Cập nhật trạng thái");
        updateStatusButton.addActionListener(this::updateTaskStatus);
        buttonPanel.add(updateStatusButton);
        
        add(buttonPanel, BorderLayout.SOUTH);
    }
    
    private void loadTasks() {
        tableModel.setRowCount(0);
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("dd/MM/yyyy");
        
        for (Project project : DataManager.getInstance().getProjects()) {
            for (Phase phase : project.getPhases()) {
                for (Task task : phase.getTasks()) {
                    // Filter tasks based on user role
                    if (currentUser.getRole() == UserRole.NHAN_VIEN && 
                        !currentUser.getId().equals(task.getAssignedTo())) {
                        continue; // Skip tasks not assigned to current employee
                    }
                    
                    User assignee = DataManager.getInstance().getUsers().stream()
                            .filter(u -> u.getId().equals(task.getAssignedTo()))
                            .findFirst().orElse(null);
                    
                    Object[] row = {
                        task.getId(),
                        task.getName(),
                        task.getDescription(),
                        assignee != null ? assignee.getName() : "Chưa phân công",
                        task.getStartDate().format(formatter),
                        task.getEndDate().format(formatter),
                        task.getStatus().getDisplayName()
                    };
                    tableModel.addRow(row);
                }
            }
        }
    }
    
    private void updateTaskStatus(ActionEvent e) {
        int selectedRow = taskTable.getSelectedRow();
        if (selectedRow >= 0) {
            String taskId = (String) tableModel.getValueAt(selectedRow, 0);
            
            // Find the task
            Task task = null;
            for (Project project : DataManager.getInstance().getProjects()) {
                for (Phase phase : project.getPhases()) {
                    for (Task t : phase.getTasks()) {
                        if (t.getId().equals(taskId)) {
                            task = t;
                            break;
                        }
                    }
                }
            }
            
            if (task != null) {
                TaskStatus[] statuses = TaskStatus.values();
                TaskStatus selectedStatus = (TaskStatus) JOptionPane.showInputDialog(
                    this,
                    "Chọn trạng thái mới:",
                    "Cập nhật trạng thái",
                    JOptionPane.QUESTION_MESSAGE,
                    null,
                    statuses,
                    task.getStatus()
                );
                
                if (selectedStatus != null) {
                    task.setStatus(selectedStatus);
                    loadTasks();
                    JOptionPane.showMessageDialog(this, "Đã cập nhật trạng thái thành công!");
                }
            }
        } else {
            JOptionPane.showMessageDialog(this, "Vui lòng chọn công việc cần cập nhật!");
        }
    }
}

// User Management Panel
class UserManagementPanel extends JPanel {
    private User currentUser;
    private JTable userTable;
    private DefaultTableModel tableModel;
    
    public UserManagementPanel(User user) {
        this.currentUser = user;
        initializeUI();
        loadUsers();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(Color.WHITE);
        
        // Header
        JPanel headerPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        headerPanel.setBackground(Color.WHITE);
        headerPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        JLabel titleLabel = new JLabel("Quản lý Nhân sự");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        titleLabel.setForeground(new Color(70, 130, 180));
        headerPanel.add(titleLabel);
        
        add(headerPanel, BorderLayout.NORTH);
        
        // Table
        String[] columns = {"ID", "Họ tên", "Tên đăng nhập", "Chức vụ"};
        tableModel = new DefaultTableModel(columns, 0) {
            @Override
            public boolean isCellEditable(int row, int column) {
                return false;
            }
        };
        
        userTable = new JTable(tableModel);
        userTable.setSelectionMode(ListSelectionModel.SINGLE_SELECTION);
        userTable.getTableHeader().setBackground(new Color(70, 130, 180));
        userTable.getTableHeader().setForeground(Color.WHITE);
        
        JScrollPane scrollPane = new JScrollPane(userTable);
        add(scrollPane, BorderLayout.CENTER);
    }
    
    private void loadUsers() {
        tableModel.setRowCount(0);
        
        for (User user : DataManager.getInstance().getUsers()) {
            Object[] row = {
                user.getId(),
                user.getName(),
                user.getUsername(),
                user.getRole().getDisplayName()
            };
            tableModel.addRow(row);
        }
    }
}

// Report Panel
class ReportPanel extends JPanel {
    private User currentUser;
    
    public ReportPanel(User user) {
        this.currentUser = user;
        initializeUI();
    }
    
    private void initializeUI() {
        setLayout(new BorderLayout());
        setBackground(Color.WHITE);
        
        // Header
        JPanel headerPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        headerPanel.setBackground(Color.WHITE);
        headerPanel.setBorder(new EmptyBorder(10, 10, 10, 10));
        
        JLabel titleLabel = new JLabel("Báo cáo & Thống kê");
        titleLabel.setFont(new Font("Arial", Font.BOLD, 18));
        titleLabel.setForeground(new Color(70, 130, 180));
        headerPanel.add(titleLabel);
        
        add(headerPanel, BorderLayout.NORTH);
        
        // Report content
        JPanel contentPanel = new JPanel(new GridLayout(2, 2, 20, 20));
        contentPanel.setBorder(new EmptyBorder(20, 20, 20, 20));
        
        // Project Statistics
        JPanel projectStats = createProjectStatsPanel();
        contentPanel.add(projectStats);
        
        // Task Statistics
        JPanel taskStats = createTaskStatsPanel();
        contentPanel.add(taskStats);
        
        // User Statistics
        JPanel userStats = createUserStatsPanel();
        contentPanel.add(userStats);
        
        // Performance Panel
        JPanel performancePanel = createPerformancePanel();
        contentPanel.add(performancePanel);
        
        add(contentPanel, BorderLayout.CENTER);
    }
    
    private JPanel createProjectStatsPanel() {
        JPanel panel = new JPanel(new BorderLayout());
        panel.setBorder(BorderFactory.createTitledBorder("Thống kê Dự án"));
        panel.setBackground(Color.WHITE);
        
        JTextArea textArea = new JTextArea();
        textArea.setEditable(false);
        textArea.setBackground(Color.WHITE);
        
        DataManager dm = DataManager.getInstance();
        StringBuilder sb = new StringBuilder();
        sb.append("Tổng số dự án: ").append(dm.getProjects().size()).append("\n");
        
        long activeProjects = dm.getProjects().stream()
                .filter(p -> p.getEndDate().isAfter(LocalDateTime.now()))
                .count();
        sb.append("Dự án đang hoạt động: ").append(activeProjects).append("\n");
        
        long completedProjects = dm.getProjects().size() - activeProjects;
        sb.append("Dự án đã hoàn thành: ").append(completedProjects
