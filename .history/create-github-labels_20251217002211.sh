#!/bin/bash

# Script to create GitHub labels for Learning-Fast-JS project
# Run this BEFORE creating issues

REPO="Tram-anh99/Learning-Fast-JS"

echo "🏷️  Creating GitHub Labels for $REPO..."
echo ""

# Check if gh CLI is installed
if ! command -v gh &> /dev/null; then
    echo "❌ GitHub CLI (gh) is not installed!"
    exit 1
fi

# Feature labels
echo "Creating feature labels..."
gh label create "enhancement" --color "a2eeef" --description "New feature or request" --repo "$REPO" 2>/dev/null || echo "✓ enhancement already exists"
gh label create "feature" --color "0e8a16" --description "New feature" --repo "$REPO" 2>/dev/null || echo "✓ feature already exists"
gh label create "camera" --color "1d76db" --description "Camera/QR scanning features" --repo "$REPO" 2>/dev/null || echo "✓ camera already exists"
gh label create "qr-code" --color "fbca04" --description "QR code functionality" --repo "$REPO" 2>/dev/null || echo "✓ qr-code already exists"
gh label create "pwa" --color "5319e7" --description "Progressive Web App" --repo "$REPO" 2>/dev/null || echo "✓ pwa already exists"
gh label create "offline" --color "c2e0c6" --description "Offline functionality" --repo "$REPO" 2>/dev/null || echo "✓ offline already exists"
gh label create "service-worker" --color "bfd4f2" --description "Service Worker implementation" --repo "$REPO" 2>/dev/null || echo "✓ service-worker already exists"
gh label create "notifications" --color "ff6f00" --description "Push notifications" --repo "$REPO" 2>/dev/null || echo "✓ notifications already exists"
gh label create "push" --color "ff9800" --description "Push notification system" --repo "$REPO" 2>/dev/null || echo "✓ push already exists"
gh label create "export" --color "006b75" --description "Export functionality" --repo "$REPO" 2>/dev/null || echo "✓ export already exists"
gh label create "pdf" --color "d93f0b" --description "PDF export" --repo "$REPO" 2>/dev/null || echo "✓ pdf already exists"
gh label create "excel" --color "217346" --description "Excel export" --repo "$REPO" 2>/dev/null || echo "✓ excel already exists"
gh label create "reporting" --color "0052cc" --description "Reporting features" --repo "$REPO" 2>/dev/null || echo "✓ reporting already exists"
gh label create "i18n" --color "c5def5" --description "Internationalization" --repo "$REPO" 2>/dev/null || echo "✓ i18n already exists"
gh label create "localization" --color "c5def5" --description "Localization support" --repo "$REPO" 2>/dev/null || echo "✓ localization already exists"
gh label create "multi-language" --color "bfd4f2" --description "Multi-language support" --repo "$REPO" 2>/dev/null || echo "✓ multi-language already exists"

# Backend labels
echo ""
echo "Creating backend labels..."
gh label create "backend" --color "d876e3" --description "Backend development" --repo "$REPO" 2>/dev/null || echo "✓ backend already exists"
gh label create "websocket" --color "5319e7" --description "WebSocket implementation" --repo "$REPO" 2>/dev/null || echo "✓ websocket already exists"
gh label create "real-time" --color "1d76db" --description "Real-time features" --repo "$REPO" 2>/dev/null || echo "✓ real-time already exists"
gh label create "sync" --color "0e8a16" --description "Data synchronization" --repo "$REPO" 2>/dev/null || echo "✓ sync already exists"
gh label create "auth" --color "d4c5f9" --description "Authentication" --repo "$REPO" 2>/dev/null || echo "✓ auth already exists"
gh label create "security" --color "ee0701" --description "Security related" --repo "$REPO" 2>/dev/null || echo "✓ security already exists"
gh label create "rbac" --color "c2e0c6" --description "Role-based access control" --repo "$REPO" 2>/dev/null || echo "✓ rbac already exists"

# Analytics & AI labels
echo ""
echo "Creating analytics labels..."
gh label create "analytics" --color "fbca04" --description "Analytics features" --repo "$REPO" 2>/dev/null || echo "✓ analytics already exists"
gh label create "charts" --color "0075ca" --description "Chart components" --repo "$REPO" 2>/dev/null || echo "✓ charts already exists"
gh label create "ai" --color "7057ff" --description "AI/ML features" --repo "$REPO" 2>/dev/null || echo "✓ ai already exists"
gh label create "ml" --color "5319e7" --description "Machine learning" --repo "$REPO" 2>/dev/null || echo "✓ ml already exists"
gh label create "pest-detection" --color "0e8a16" --description "Pest detection AI" --repo "$REPO" 2>/dev/null || echo "✓ pest-detection already exists"
gh label create "tensorflow" --color "ff6f00" --description "TensorFlow.js" --repo "$REPO" 2>/dev/null || echo "✓ tensorflow already exists"

# Mobile & Performance labels
echo ""
echo "Creating mobile/performance labels..."
gh label create "mobile" --color "d876e3" --description "Mobile app" --repo "$REPO" 2>/dev/null || echo "✓ mobile already exists"
gh label create "react-native" --color "61dafb" --description "React Native" --repo "$REPO" 2>/dev/null || echo "✓ react-native already exists"
gh label create "ios" --color "000000" --description "iOS platform" --repo "$REPO" 2>/dev/null || echo "✓ ios already exists"
gh label create "android" --color "3ddc84" --description "Android platform" --repo "$REPO" 2>/dev/null || echo "✓ android already exists"
gh label create "performance" --color "fbca04" --description "Performance improvements" --repo "$REPO" 2>/dev/null || echo "✓ performance already exists"
gh label create "map" --color "0075ca" --description "Map/GIS features" --repo "$REPO" 2>/dev/null || echo "✓ map already exists"
gh label create "optimization" --color "1d76db" --description "Code optimization" --repo "$REPO" 2>/dev/null || echo "✓ optimization already exists"

# Testing & Quality labels
echo ""
echo "Creating testing labels..."
gh label create "testing" --color "d4c5f9" --description "Testing related" --repo "$REPO" 2>/dev/null || echo "✓ testing already exists"
gh label create "vitest" --color "729b1b" --description "Vitest unit tests" --repo "$REPO" 2>/dev/null || echo "✓ vitest already exists"
gh label create "unit-tests" --color "c2e0c6" --description "Unit testing" --repo "$REPO" 2>/dev/null || echo "✓ unit-tests already exists"
gh label create "e2e" --color "0e8a16" --description "End-to-end tests" --repo "$REPO" 2>/dev/null || echo "✓ e2e already exists"
gh label create "playwright" --color "d73a4a" --description "Playwright E2E" --repo "$REPO" 2>/dev/null || echo "✓ playwright already exists"
gh label create "quality" --color "0052cc" --description "Code quality" --repo "$REPO" 2>/dev/null || echo "✓ quality already exists"

# Phase labels
echo ""
echo "Creating phase labels..."
gh label create "phase-2" --color "d876e3" --description "Phase 2 (Q1 2026)" --repo "$REPO" 2>/dev/null || echo "✓ phase-2 already exists"
gh label create "phase-3" --color "5319e7" --description "Phase 3 (Q2 2026)" --repo "$REPO" 2>/dev/null || echo "✓ phase-3 already exists"

# Priority labels (default GitHub labels, just ensure they exist)
echo ""
echo "Ensuring priority labels exist..."
gh label create "priority: high" --color "d73a4a" --description "High priority" --repo "$REPO" 2>/dev/null || echo "✓ priority: high already exists"
gh label create "priority: medium" --color "fbca04" --description "Medium priority" --repo "$REPO" 2>/dev/null || echo "✓ priority: medium already exists"
gh label create "priority: low" --color "0e8a16" --description "Low priority" --repo "$REPO" 2>/dev/null || echo "✓ priority: low already exists"

echo ""
echo "✅ All labels created successfully!"
echo "🔗 View labels at: https://github.com/$REPO/labels"
