# Frontend Testing Checklist - Phase 5

## Responsive Design Testing (Step 10)

### Mobile (375px - 414px)
- [ ] **Home Page**
  - [ ] Header displays correctly
  - [ ] Hero text is readable
  - [ ] Lead form fields stack vertically
  - [ ] Product interests are manageable
  - [ ] Submit button is accessible
  - [ ] Footer displays properly

- [ ] **Admin Page**
  - [ ] Navigation tabs wrap or scroll
  - [ ] Dashboard cards stack vertically
  - [ ] Charts are readable
  - [ ] Leads table scrolls horizontally
  - [ ] Approval queue is accessible

### Tablet (768px - 1024px)
- [ ] **Home Page**
  - [ ] Form uses 2-column grid where appropriate
  - [ ] Spacing is comfortable
  - [ ] All elements visible without scrolling excessively

- [ ] **Admin Page**
  - [ ] Dashboard shows 2 cards per row
  - [ ] Charts display side-by-side
  - [ ] Table columns are readable
  - [ ] Navigation is clear

### Desktop (1920px+)
- [ ] **Home Page**
  - [ ] Form is centered and max-width applied
  - [ ] No excessive whitespace
  - [ ] Typography scales appropriately

- [ ] **Admin Page**
  - [ ] Dashboard shows 4 cards per row
  - [ ] Charts utilize full width
  - [ ] Table is fully visible
  - [ ] All content is accessible

### Touch Targets
- [ ] All buttons are at least 44x44px
- [ ] Links are easily tappable
- [ ] Form inputs have adequate padding
- [ ] Dropdowns work on touch devices

---

## Final Integration Testing (Step 11)

### 1. Public Lead Submission Flow
**Test Case**: Submit a new lead from the public form

**Steps**:
1. Navigate to http://localhost:5173/
2. Fill out the lead form:
   - Name: "Test User"
   - Email: "test@example.com"
   - Phone: "+91 9876543210"
   - Role: "Architect"
   - Location: "Mumbai"
   - Add product: Category "Flooring", Product "Premium Laminate"
   - Message: "Need urgent quote for 5000 sq ft project"
3. Click "Submit Inquiry"

**Expected Results**:
- [ ] Form validates required fields
- [ ] Loading state shows during submission
- [ ] Success message displays
- [ ] Form resets after submission
- [ ] Backend receives lead (check terminal logs)
- [ ] AI categorization runs
- [ ] Email is sent (check backend logs)
- [ ] Lead appears in admin panel

---

### 2. Admin Dashboard Verification
**Test Case**: View dashboard metrics and charts

**Steps**:
1. Navigate to http://localhost:5173/admin
2. Verify Dashboard tab is active by default
3. Check all stat cards display numbers
4. Verify charts render correctly

**Expected Results**:
- [ ] Total Leads count is accurate
- [ ] New Today shows correct count
- [ ] Pending Follow-ups displays
- [ ] SLA Violations shows (should be 0 initially)
- [ ] Bar chart renders with data
- [ ] Pie chart shows status distribution
- [ ] Metric cards display values
- [ ] Dashboard auto-refreshes every 30s
- [ ] Real-time updates work (submit new lead and watch dashboard update)

---

### 3. Leads Management
**Test Case**: Search, filter, and view leads

**Steps**:
1. Go to Admin panel → Leads tab
2. Verify leads table displays
3. Use search box to search by name
4. Use status filter dropdown
5. Click "View" on a lead

**Expected Results**:
- [ ] All leads display in table
- [ ] Search filters results correctly
- [ ] Status filter works
- [ ] Status badges are color-coded
- [ ] Created date formats correctly
- [ ] View button is clickable (placeholder for now)

---

### 4. Approval Queue Management
**Test Case**: View and manage approvals

**Steps**:
1. Go to Admin panel → Approvals tab
2. Check for pending approvals
3. If approvals exist, click "Approve" on one
4. Click "Reject" on another (enter reason)

**Expected Results**:
- [ ] Pending approvals list displays
- [ ] Count is accurate
- [ ] Metadata displays in readable format
- [ ] Approve action works
- [ ] Reject prompts for reason
- [ ] List refreshes after action
- [ ] "No pending approvals" shows when empty

---

### 5. Navigation & Routing
**Test Case**: Navigate between pages

**Steps**:
1. Start at home page (/)
2. Navigate to /admin
3. Switch between tabs
4. Use browser back button
5. Refresh page on each route

**Expected Results**:
- [ ] Routes work correctly
- [ ] Tab state persists during navigation
- [ ] Browser back/forward works
- [ ] Page refresh maintains route
- [ ] No console errors

---

### 6. Error Handling
**Test Case**: Test error scenarios

**Steps**:
1. Stop backend server
2. Try to submit a lead
3. Try to load admin dashboard
4. Restart backend

**Expected Results**:
- [ ] Error messages display clearly
- [ ] No app crashes
- [ ] Retry functionality works (if implemented)
- [ ] App recovers when backend restarts

---

### 7. Performance Check
**Test Case**: Verify app performance

**Steps**:
1. Open browser DevTools → Network tab
2. Load home page
3. Load admin page
4. Check console for errors

**Expected Results**:
- [ ] Pages load in < 2 seconds
- [ ] No console errors
- [ ] No console warnings (except expected ones)
- [ ] Charts animate smoothly
- [ ] No memory leaks (check DevTools Memory tab)

---

### 8. Cross-Browser Testing
**Test Case**: Verify compatibility

**Browsers to Test**:
- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (if on Mac)
- [ ] Edge (latest)

**Expected Results**:
- [ ] All features work in each browser
- [ ] Styling is consistent
- [ ] No browser-specific errors

---

## Test Results Summary

### Passed Tests
- List tests that passed

### Failed Tests
- List tests that failed with details

### Known Issues
- Document any known issues or limitations

### Notes
- Any additional observations or recommendations

---

## Sign-off

**Tester**: _______________  
**Date**: _______________  
**Phase 5 Status**: ⬜ Complete ⬜ Needs Work  

**Comments**:
