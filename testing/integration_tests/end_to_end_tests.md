# End-to-End Integration Tests

**Tester:** Rishi Nalam  
**Purpose:** Test complete user journeys

---

## Test Suite 1: New User Journey

### Test 1.1: Complete Flow
**Steps:**
1. Open browser to `http://localhost:5173/`
2. Click "Get Started" button
3. Dashboard should load with demo data
4. Navigate to "Log Activity"
5. Fill form with valid data:
   - Activity Type: "Work"
   - Duration: 60 minutes
   - Productivity Score: 8
   - Focus Level: "High"
6. Submit form
7. Return to dashboard
8. Verify new activity appears

**Expected Result:**
- Clean navigation flow
- All data loads successfully
- Activity saves and displays

**Status:** ⬜ Pass / ⬜ Fail  
**Notes:** _________________________________

---

## Test Suite 2: API Integration

### Test 2.1: Frontend-Backend Connection
**Steps:**
1. Open DevTools → Network tab
2. Navigate to dashboard
3. Verify API calls:
   - `GET /api/dashboard/1` → 200 OK
   - `GET /api/predictions/1` → 200 OK
   - `GET /api/recommendations/1` → 200 OK

**Expected Result:**
- All API calls succeed
- Response data correct format
- No CORS errors

**Status:** ⬜ Pass / ⬜ Fail

---

## Test Suite 3: ML Integration

### Test 3.1: Predictions Work
**Steps:**
1. Navigate to dashboard
2. Verify predictions chart displays
3. Check DevTools for ML-related errors
4. Verify predictions API response

**Expected Response:**
```json
{
  "hourly_predictions": [
    {"hour": 0, "predicted_score": 3.2},
    ...
  ],
  "peak_hours": [9, 10, 14, 15]
}
```

**Status:** ⬜ Pass / ⬜ Fail

---

## Test Suite 4: Error Handling

### Test 4.1: Backend Down
**Steps:**
1. Stop backend server
2. Navigate to dashboard
3. Observe error handling
4. Restart backend
5. Verify app recovers

**Expected Result:**
- Friendly error message shows
- No crashes
- Recovers when backend is back

**Status:** ⬜ Pass / ⬜ Fail

---

## ��� Integration Test Summary

**Tests Passed:** _____  
**Tests Failed:** _____  
**Critical Issues:** _____

**Ready for Production:** ⬜ Yes / ⬜ No
