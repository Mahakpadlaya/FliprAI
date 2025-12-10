# Deploying FliprAI to Vercel

This guide will help you deploy your FliprAI application to Vercel.

## Prerequisites

1. A GitHub account with the FliprAI repository
2. A Vercel account (sign up at https://vercel.com)
3. MongoDB Atlas connection string (for the database)

## Deployment Steps

### 1. Push Changes to GitHub

Make sure all changes are committed and pushed to your GitHub repository:

```bash
git add .
git commit -m "Configure for Vercel deployment"
git push origin main
```

### 2. Connect to Vercel

1. Go to [Vercel Dashboard](https://vercel.com/dashboard)
2. Click "Add New..." → "Project"
3. Import your GitHub repository: `Mahakpadlaya/FliprAI`
4. Click "Import"

### 3. Configure Project Settings

Vercel should auto-detect the settings, but verify:

- **Framework Preset**: Other
- **Root Directory**: `./` (root)
- **Build Command**: Leave empty (no build needed for this project)
- **Output Directory**: Leave empty

### 4. Add Environment Variables

In the "Environment Variables" section, add:

- `MONGODB_URI`: Your MongoDB Atlas connection string
  - Example: `mongodb+srv://username:password@cluster.mongodb.net/`
- `DB_NAME`: `fullstack-task` (or your preferred database name)

### 5. Deploy

Click "Deploy" and wait for the deployment to complete.

### 6. Access Your Application

Once deployed, Vercel will provide you with a URL like:
- `https://fliprai.vercel.app`
- `https://fliprai-<random>.vercel.app`

## Important Notes

### Image Storage
The current Vercel setup stores images as base64 strings in MongoDB. For production with large images, consider:
- Using Cloudinary or AWS S3 for image storage
- Updating the API to use external image hosting

### Serverless Function Limits
- Vercel serverless functions have execution time limits
- Image processing happens in-memory (base64 conversion)
- Large images may cause timeout issues

### Local Development
- For local development, continue using `python app.py` in the `backend` folder
- The frontend will automatically detect the environment and use the correct API URL

## Troubleshooting

### Build Errors
- Check that all Python dependencies are in `api/requirements.txt`
- Verify environment variables are set correctly

### API Errors
- Check MongoDB connection string is correct
- Verify environment variables are set in Vercel dashboard
- Check Vercel function logs in the dashboard

### Image Upload Issues
- Images are converted to base64 for Vercel deployment
- Large images (>5MB) may fail
- Check browser console for errors

## Updating Your Deployment

Every time you push to the `main` branch on GitHub, Vercel will automatically redeploy your application.

## Custom Domain (Optional)

1. Go to your project settings in Vercel
2. Click "Domains"
3. Add your custom domain
4. Follow DNS configuration instructions

