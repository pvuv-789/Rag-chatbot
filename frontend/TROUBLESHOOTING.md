# Frontend Troubleshooting Guide

## Issue: Tailwind CSS PostCSS Error

### Error Message
```
[postcss] It looks like you're trying to use `tailwindcss` directly as a PostCSS plugin.
The PostCSS plugin has moved to a separate package...
```

### Cause
This happens when Tailwind CSS v4 is installed instead of v3. Tailwind v4 has breaking changes with PostCSS configuration.

### Solution

**Step 1: Uninstall Tailwind v4**
```bash
cd frontend
npm uninstall tailwindcss postcss autoprefixer
```

**Step 2: Install Tailwind v3**
```bash
npm install -D tailwindcss@3 postcss autoprefixer
```

**Step 3: Verify Installation**
```bash
npm list tailwindcss
```

Should show: `tailwindcss@3.x.x`

**Step 4: Start Dev Server**
```bash
npm run dev
```

## Other Common Issues

### Issue: Port 5173 Already in Use

**Symptom**: Error message or server starts on different port (5174, 5175, etc.)

**Solution**: This is normal! Vite will automatically use the next available port. Just use the URL shown in the terminal.

### Issue: "Cannot find module 'axios'"

**Solution**:
```bash
npm install axios
```

### Issue: Styles Not Loading

**Solution 1: Clear Vite Cache**
```bash
rm -rf node_modules/.vite
npm run dev
```

**Solution 2: Rebuild Tailwind**
```bash
npm run dev
# Press Ctrl+C
npm run dev
```

### Issue: Module Not Found Errors

**Solution**:
```bash
# Delete node_modules and reinstall
rm -rf node_modules
rm package-lock.json
npm install
```

### Issue: Browser Shows Blank Page

**Check**:
1. Open browser DevTools (F12)
2. Check Console tab for errors
3. Check Network tab for failed requests

**Common fixes**:
- Clear browser cache (Ctrl+Shift+Delete)
- Hard refresh (Ctrl+Shift+R)
- Check if backend is running

### Issue: CORS Errors

**Error**: "Access to fetch at 'http://localhost:8000' has been blocked by CORS policy"

**Solution**: Make sure backend is running and CORS is configured correctly.

Check `backend/main.py`:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Verification Checklist

- [ ] Node.js 18+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] Dependencies installed (`npm install`)
- [ ] Tailwind CSS v3 installed (`npm list tailwindcss`)
- [ ] Dev server starts without errors
- [ ] Browser opens to localhost:5173 or 5174
- [ ] No console errors in browser DevTools

## Clean Install (Nuclear Option)

If nothing else works:

```bash
cd frontend

# Delete everything
rm -rf node_modules
rm package-lock.json

# Reinstall
npm install

# Reinstall Tailwind specifically
npm install -D tailwindcss@3 postcss autoprefixer

# Start
npm run dev
```

## Check Package Versions

Run this to see all installed versions:

```bash
npm list --depth=0
```

Expected versions:
- react: 18.x
- vite: 7.x
- tailwindcss: 3.x
- axios: 1.x

## Getting Help

1. Check browser console (F12)
2. Check terminal output
3. Verify backend is running on port 8000
4. Try the clean install steps above

## Success Indicators

✅ Terminal shows: `VITE v7.x.x ready in XXXms`
✅ Terminal shows: `Local: http://localhost:5173/` (or 5174)
✅ Browser opens and shows chat interface
✅ No errors in browser console
✅ Tailwind styles are applied (UI looks styled)

## Quick Test

After starting the dev server, you should see:
1. A header with "RAG Chatbot"
2. "Upload PDF" button in the top right
3. A chat input at the bottom
4. Nice styling with colors and spacing

If you see this, everything is working! 🎉
