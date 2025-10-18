# Frontend Manual Testing Checklist

**Tester:** Rishi Nalam  
**Frontend Framework:** React + Vite  
**Status:** ✅ Ready for Testing

---

## 1. Landing Page Tests

### 1.1 Initial Load
- [ ] Page loads within 3 seconds
- [ ] All images load correctly
- [ ] Hero section displays with correct text
- [ ] CTA button ("Get Started") is visible
- [ ] Navigation bar displays properly
- [ ] No console errors in DevTools

**Test URL:** `http://localhost:5173/`

**Status:** ⬜ Pass / ⬜ Fail  
**Notes:** _________________________________

---

### 1.2 Responsive Design
- [ ] Test on mobile (375px width)
- [ ] Test on tablet (768px width)
- [ ] Test on desktop (1920px width)
- [ ] All text is readable on all sizes
- [ ] Images resize appropriately
- [ ] No horizontal scrolling
- [ ] Buttons are easily tappable on mobile

**How to Test:**
1. Open Chrome DevTools (F12)
2. Click device toolbar icon (Ctrl+Shift+M)
3. Test different device sizes

**Status:** ⬜ Pass / ⬜ Fail

---

### 1.3 Navigation
- [ ] "Get Started" button works
- [ ] Redirects to dashboard
- [ ] Navigation is smooth (no page refresh)
- [ ] Browser back button works

**Status:** ⬜ Pass / ⬜ Fail

---

## 2. Dashboard Tests

### 2.1 Initial Load
- [ ] Dashboard loads within 2 seconds
- [ ] All stat cards display (4 cards)
- [ ] Chart/graph renders correctly
- [ ] Recommendations section loads
- [ ] Today's productivity score shows
- [ ] Work time displays
- [ ] Break time displays
- [ ] Focus time displays
- [ ] No console errors

**Test URL:** `http://localhost:5173/dashboard`

**Status:** ⬜ Pass / ⬜ Fail

---

### 2.2 Data Display
- [ ] Productivity score is a number (0-10)
- [ ] Work time is in hours
- [ ] Chart has proper labels
- [ ] Chart has proper data points
- [ ] Colors are consistent
- [ ] Numbers are formatted correctly

**Status:** ⬜ Pass / ⬜ Fail

---

### 2.3 Recommendations
- [ ] At least 3 recommendations display
- [ ] Each has an icon
- [ ] Each has a title
- [ ] Each has a description
- [ ] Priority levels shown (high/medium/low)
- [ ] Recommendations are readable

**Status:** ⬜ Pass / ⬜ Fail

---

## 3. Activity Logging Tests

### 3.1 Form Display
- [ ] Activity log form loads
- [ ] All form fields are present:
  - [ ] Activity type dropdown
  - [ ] Duration input
  - [ ] Productivity score slider/input
  - [ ] Focus level selection
  - [ ] Notes textarea
- [ ] Form labels are clear
- [ ] Submit button is visible

**Test URL:** `http://localhost:5173/log-activity`

**Status:** ⬜ Pass / ⬜ Fail

---

### 3.2 Form Validation
- [ ] Cannot submit empty form
- [ ] Activity type is required
- [ ] Duration must be positive number
- [ ] Productivity score: 0-10 only
- [ ] Error messages display for invalid input

**Test Cases:**
1. Empty form → Should show errors
2. Duration = -10 → Should show error
3. Score = 15 → Should show error
4. All valid → Should succeed

**Status:** ⬜ Pass / ⬜ Fail

---

### 3.3 Form Submission
- [ ] Valid form submits successfully
- [ ] Success message displays
- [ ] Form clears after submission
- [ ] Can submit multiple activities
- [ ] Loading indicator shows during submit

**Status:** ⬜ Pass / ⬜ Fail

---

## 4. API Integration Tests

### 4.1 Backend Connection
- [ ] Frontend connects to backend
- [ ] Dashboard fetches data successfully
- [ ] Activity logging sends data to backend
- [ ] Loading states display during API calls

**How to Test:**
1. Open DevTools → Network tab
2. Refresh dashboard
3. Look for API calls to backend
4. Verify requests return 200 status

**Expected API Calls:**
- `GET /api/dashboard/1`
- `GET /api/predictions/1`
- `GET /api/recommendations/1`
- `POST /api/activities/log`

**Status:** ⬜ Pass / ⬜ Fail

---

## 5. Performance Tests

### 5.1 Load Times
- [ ] Landing page loads < 2 seconds
- [ ] Dashboard loads < 3 seconds
- [ ] Page transitions are smooth
- [ ] Charts render quickly

**Measure:**
1. Open DevTools → Network tab
2. Check "Disable cache"
3. Reload page
4. Look at Load time

**Target:** < 3 seconds

**Status:** ⬜ Pass / ⬜ Fail

---

## 6. Browser Compatibility Tests

### 6.1 Chrome
- [ ] All features work
- [ ] Layout is correct
- [ ] No console errors
- [ ] Charts render correctly

**Status:** ⬜ Pass / ⬜ Fail

---

### 6.2 Firefox
- [ ] All features work
- [ ] Layout is correct
- [ ] No console errors

**Status:** ⬜ Pass / ⬜ Fail

---

## ��� Testing Summary

**Total Tests:** 50+  
**Tests Passed:** _____  
**Tests Failed:** _____  
**Pass Rate:** _____%

---

## ��� Bugs Found

### Critical Bugs
1. _________________________________
2. _________________________________

### Medium Priority Bugs
1. _________________________________
2. _________________________________

### Low Priority Bugs
1. _________________________________

---

## ✅ Final Sign-Off

**All critical tests passed:** ⬜ Yes / ⬜ No  
**Ready for deployment:** ⬜ Yes / ⬜ No  
**Tested by:** Rishi Nalam  
**Date:** ______________
