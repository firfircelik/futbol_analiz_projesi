# 🚀 ScoutAI - Deployment Guide

## Launch Your SaaS in 30 Minutes

This guide will take you from zero to production with a revenue-generating SaaS application.

---

## Prerequisites

- **Server:** DigitalOcean Droplet ($12/month), AWS EC2, or any VPS
- **Domain:** Your domain (e.g., scoutai.com)
- **Stripe Account:** For payments
- **10 minutes:** That's all the time you need

---

## Quick Deploy (Docker)

### Step 1: Clone & Setup (2 minutes)

```bash
# On your server
git clone https://github.com/firfircelik/futbol_analiz_projesi.git
cd futbol_analiz_projesi

# Copy environment file
cp .env.example .env

# Edit environment variables
nano .env
```

### Step 2: Configure Environment (3 minutes)

Edit `.env`:

```bash
# Database
DB_PASSWORD=your_strong_password_here

# JWT Authentication
JWT_SECRET_KEY=your_random_secret_key_here  # Generate with: openssl rand -hex 32

# Stripe (get from https://dashboard.stripe.com/apikeys)
STRIPE_API_KEY=sk_live_xxxxx
STRIPE_WEBHOOK_SECRET=whsec_xxxxx

# Email (optional, for now)
SMTP_HOST=smtp.sendgrid.net
SMTP_PORT=587
SMTP_USER=apikey
SMTP_PASSWORD=your_sendgrid_api_key

# Application
ENV=production
DOMAIN=scoutai.com
```

### Step 3: Start Services (5 minutes)

```bash
# Build and start
docker-compose up -d

# Check logs
docker-compose logs -f api

# Verify it's running
curl http://localhost:8000/
```

You should see: `{"service": "ScoutAI API", "status": "operational"}`

### Step 4: Setup Stripe Products (10 minutes)

1. Go to https://dashboard.stripe.com/products
2. Create products for each tier:

**Scout Plan:**
- Name: Scout
- Price: €29/month (recurring)
- Copy the Price ID → Update `app/config/products.py`

**Professional Plan:**
- Name: Professional
- Price: €99/month (recurring)
- Copy the Price ID → Update `app/config/products.py`

**Club Plan:**
- Name: Club
- Price: €299/month (recurring)
- Copy the Price ID → Update `app/config/products.py`

3. Setup webhook:
   - Go to https://dashboard.stripe.com/webhooks
   - Add endpoint: `https://yourdomain.com/api/webhooks/stripe`
   - Select events: `customer.subscription.*`, `invoice.*`
   - Copy webhook secret → Add to `.env` as `STRIPE_WEBHOOK_SECRET`

### Step 5: Setup Domain & SSL (10 minutes)

```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get SSL certificate
sudo certbot --nginx -d scoutai.com -d www.scoutai.com

# Auto-renew
sudo certbot renew --dry-run
```

Update `nginx.conf`:

```nginx
server {
    listen 80;
    server_name scoutai.com www.scoutai.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name scoutai.com www.scoutai.com;

    ssl_certificate /etc/letsencrypt/live/scoutai.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/scoutai.com/privkey.pem;

    # Static files (landing page)
    location / {
        root /usr/share/nginx/html;
        try_files $uri $uri/ /index.html;
    }

    # API
    location /api {
        proxy_pass http://api:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Restart nginx:
```bash
docker-compose restart nginx
```

---

## You're Live! 🎉

Your SaaS is now running at:
- **Landing Page:** https://scoutai.com
- **API:** https://scoutai.com/api/docs
- **Admin:** Coming soon

---

## Production Checklist

### Security ✅

- [ ] Strong passwords in `.env`
- [ ] JWT secret is random (32+ characters)
- [ ] SSL certificate installed
- [ ] Firewall configured (UFW)
- [ ] Database not exposed publicly
- [ ] Stripe in live mode
- [ ] Rate limiting enabled

### Monitoring ✅

- [ ] Setup Sentry (error tracking)
- [ ] Setup health checks
- [ ] Setup uptime monitoring (UptimeRobot)
- [ ] Setup log aggregation

### Payments ✅

- [ ] Stripe products created
- [ ] Webhook configured
- [ ] Test subscription flow
- [ ] Setup tax collection (if required)

### Marketing ✅

- [ ] Google Analytics installed
- [ ] Metadata optimized (SEO)
- [ ] Social cards configured
- [ ] Newsletter signup
- [ ] First 100 users target

---

## Scaling Guide

### When you hit 1,000 users:

```yaml
# docker-compose.yml - Update to 3 API instances
api:
  deploy:
    replicas: 3

# Add Redis for caching
redis:
  image: redis:7-alpine
  command: redis-server --maxmemory 2gb --maxmemory-policy allkeys-lru
```

### When you hit 10,000 users:

- Upgrade to managed PostgreSQL (DigitalOcean Managed Database)
- Add CDN (Cloudflare)
- Horizontal scaling (Load balancer + multiple servers)
- Consider Kubernetes

---

## Cost Breakdown

### Month 1 (MVP)

| Service | Cost/Month |
|---------|------------|
| DigitalOcean Droplet (2 CPU, 4GB RAM) | $24 |
| Domain (.com) | $12/year = $1 |
| SSL Certificate | Free (Let's Encrypt) |
| Stripe | 2.9% + €0.30 per transaction |
| SendGrid (email) | Free tier (100/day) |
| **Total** | **~$25/month** |

### Month 6 (1,000 users, €30k MRR)

| Service | Cost/Month |
|---------|------------|
| DigitalOcean (8 CPU, 16GB RAM) | $96 |
| Managed PostgreSQL | $60 |
| Redis Cache | $15 |
| CDN (Cloudflare Pro) | $20 |
| SendGrid (50k emails/month) | $20 |
| Monitoring (Sentry) | $26 |
| Stripe fees (€30k × 2.9%) | $870 |
| **Total** | **~$1,100/month** |

**Profit Margin:** 96% (before marketing & salaries)

### Month 12 (3,000 users, €60k MRR)

- Infrastructure: ~$2,000/month
- Gross Margin: 97%
- Net Margin (after marketing): 60-70%

**This is a SOFTWARE business - scales beautifully!**

---

## Common Issues & Fixes

### API won't start

```bash
# Check logs
docker-compose logs api

# Common fix: database not ready
docker-compose restart db
docker-compose up -d api
```

### Can't connect to database

```bash
# Test database connection
docker-compose exec db psql -U scoutai -d scoutai

# Reset database
docker-compose down -v
docker-compose up -d
```

### Stripe webhooks failing

```bash
# Test locally with Stripe CLI
stripe listen --forward-to localhost:8000/api/webhooks/stripe

# Check webhook signature in logs
docker-compose logs api | grep stripe
```

---

## Maintenance

### Daily Tasks

```bash
# Check application health
curl https://scoutai.com/api/v1/stats

# Check error logs
docker-compose logs --tail=100 api | grep ERROR
```

### Weekly Tasks

```bash
# Backup database
docker-compose exec db pg_dump -U scoutai scoutai > backup_$(date +%Y%m%d).sql

# Update dependencies
docker-compose pull
docker-compose up -d
```

### Monthly Tasks

- Review Stripe dashboard (revenue, churn)
- Check uptime statistics
- Review user feedback
- Plan new features
- Optimize slow queries

---

## Getting Your First Users

### Week 1: Soft Launch

1. **Friends & Family** (10 users)
   - Free access for feedback
   - Ask for testimonials

2. **Reddit** (50 users)
   - Post in r/footballmanagers, r/FantasyPL
   - Offer launch discount: 50% off first month
   - Collect feedback

3. **Twitter/X** (20 users)
   - Thread about building in public
   - Share insights ("Here's what we found about...")
   - Tag relevant accounts

### Week 2-4: Public Launch

1. **Product Hunt** (200 users)
   - Prepare launch
   - Get upvotes from network
   - Respond to every comment

2. **Direct Outreach** (30 clubs)
   - Email lower league clubs
   - Offer free trial
   - Case study if they succeed

3. **Content Marketing** (100 users)
   - "How We Found This Player Before Everyone Else"
   - Weekly undervalued player analysis
   - SEO-optimized blog posts

**Goal:** 100 paying users by Month 3 = €5,000 MRR

---

## When to Hire

### Month 1-3: Solo
- You can handle everything
- Use no-code tools where possible
- Focus on product & customers

### Month 4-6: First Hire
- **Customer Success** (part-time)
- Handle support tickets
- Onboard new users

### Month 7-12: Small Team
- **Full-stack Developer** (full-time)
- **Marketing** (part-time contractor)
- Keep it lean!

### Year 2: Scale
- Sales team (for Enterprise)
- Data team (for coverage expansion)
- DevOps (for infrastructure)

---

## Exit Strategy

### Year 1: Prove It Works
- €500k-€1M ARR
- 500-1,000 paying customers
- 60-70% gross margins
- Strong retention (>90%)

### Year 2: Scale It
- €2M-€5M ARR
- 2,000-5,000 customers
- International expansion
- Enterprise deals

### Year 3: Exit or Continue

**Acquisition Targets:**
- Opta/Stats Perform
- StatsBomb
- Wyscout
- Sports media companies
- Betting operators

**Typical Valuation:** 5-10x ARR for SaaS

Example: €5M ARR × 7x = **€35M exit**

Or keep running it and make €2-3M/year profit 💰

---

## Support

**Technical Issues:**
- GitHub Issues: https://github.com/firfircelik/futbol_analiz_projesi/issues
- Discord: [Your community]
- Email: support@scoutai.com

**Sales & Enterprise:**
- Email: sales@scoutai.com
- Book a call: calendly.com/scoutai

---

**You've got this. Now go make money! 💰**
