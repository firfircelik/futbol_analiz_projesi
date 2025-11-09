"""
Product Configuration & Pricing Tiers
Defines all subscription plans and their features
"""

from enum import Enum
from dataclasses import dataclass
from typing import List, Optional, Tuple


class PlanTier(str, Enum):
    """Subscription plan tiers."""
    FREE = "free"
    SCOUT = "scout"
    PROFESSIONAL = "professional"
    CLUB = "club"
    ENTERPRISE = "enterprise"


@dataclass
class PlanFeatures:
    """Features included in a plan."""
    # Core features
    player_reports_per_month: int
    leagues_access: int  # Number of leagues
    team_fit_analyses_per_month: int
    api_requests_per_month: int

    # Advanced features
    advanced_metrics: bool = False  # xG, xA, PPDA, etc.
    moneyball_valuation: bool = False
    pdf_exports: bool = False
    excel_exports: bool = False
    email_reports: bool = False

    # Team features
    multi_user_seats: int = 1
    white_label_reports: bool = False
    custom_integrations: bool = False
    priority_support: bool = False
    dedicated_account_manager: bool = False

    # API features
    api_access: bool = False
    webhook_support: bool = False
    custom_endpoints: bool = False

    # Live features
    live_match_analysis: bool = False
    real_time_alerts: bool = False


@dataclass
class PlanPricing:
    """Pricing information for a plan."""
    tier: PlanTier
    name: str
    description: str
    price_monthly_eur: float
    price_yearly_eur: float  # Usually monthly * 10 (2 months free)
    stripe_price_id_monthly: Optional[str] = None
    stripe_price_id_yearly: Optional[str] = None
    currency: str = "EUR"
    billing_period: str = "month"

    @property
    def yearly_savings_percent(self) -> int:
        """Calculate percentage saved with yearly billing."""
        if self.price_monthly_eur == 0:
            return 0
        monthly_total = self.price_monthly_eur * 12
        savings = ((monthly_total - self.price_yearly_eur) / monthly_total) * 100
        return int(savings)


# =====================================================
# PRODUCT DEFINITIONS
# =====================================================

PLANS = {
    PlanTier.FREE: {
        "pricing": PlanPricing(
            tier=PlanTier.FREE,
            name="Free",
            description="Try out ScoutAI with limited features",
            price_monthly_eur=0,
            price_yearly_eur=0,
        ),
        "features": PlanFeatures(
            player_reports_per_month=10,
            leagues_access=3,  # EPL, La Liga, Bundesliga only
            team_fit_analyses_per_month=0,
            api_requests_per_month=0,
            advanced_metrics=False,
            moneyball_valuation=False,
            pdf_exports=False,
            excel_exports=False,
            api_access=False,
        ),
        "target_audience": "Casual fans, testing the platform",
        "call_to_action": "Upgrade to Scout for unlimited reports",
    },

    PlanTier.SCOUT: {
        "pricing": PlanPricing(
            tier=PlanTier.SCOUT,
            name="Scout",
            description="Perfect for amateur scouts and fantasy football enthusiasts",
            price_monthly_eur=29,
            price_yearly_eur=290,  # 2 months free
            stripe_price_id_monthly="price_scout_monthly",  # Replace with actual Stripe ID
            stripe_price_id_yearly="price_scout_yearly",
        ),
        "features": PlanFeatures(
            player_reports_per_month=100,
            leagues_access=10,  # Top 10 leagues
            team_fit_analyses_per_month=10,
            api_requests_per_month=1000,
            advanced_metrics=False,
            moneyball_valuation=False,
            pdf_exports=True,
            excel_exports=False,
            api_access=True,
            email_reports=False,
        ),
        "target_audience": "Amateur scouts, fantasy players, content creators",
        "call_to_action": "Most popular for individual users",
        "popular": True,
    },

    PlanTier.PROFESSIONAL: {
        "pricing": PlanPricing(
            tier=PlanTier.PROFESSIONAL,
            name="Professional",
            description="For serious analysts, agents, and lower league clubs",
            price_monthly_eur=99,
            price_yearly_eur=990,  # 2 months free
            stripe_price_id_monthly="price_professional_monthly",
            stripe_price_id_yearly="price_professional_yearly",
        ),
        "features": PlanFeatures(
            player_reports_per_month=500,
            leagues_access=50,  # 50+ leagues
            team_fit_analyses_per_month=999999,  # Unlimited
            api_requests_per_month=10000,
            advanced_metrics=True,  # xG, xA, PPDA, etc.
            moneyball_valuation=True,
            pdf_exports=True,
            excel_exports=True,
            email_reports=True,
            api_access=True,
            priority_support=True,
        ),
        "target_audience": "Professional scouts, agents, lower league clubs, analysts",
        "call_to_action": "Best value for professionals",
        "popular": True,
        "recommended": True,
    },

    PlanTier.CLUB: {
        "pricing": PlanPricing(
            tier=PlanTier.CLUB,
            name="Club",
            description="For professional clubs and agencies",
            price_monthly_eur=299,
            price_yearly_eur=2990,  # 2 months free
            stripe_price_id_monthly="price_club_monthly",
            stripe_price_id_yearly="price_club_yearly",
        ),
        "features": PlanFeatures(
            player_reports_per_month=999999,  # Unlimited
            leagues_access=999,  # All leagues
            team_fit_analyses_per_month=999999,  # Unlimited
            api_requests_per_month=100000,
            advanced_metrics=True,
            moneyball_valuation=True,
            pdf_exports=True,
            excel_exports=True,
            email_reports=True,
            api_access=True,
            webhook_support=True,
            multi_user_seats=5,
            white_label_reports=True,
            custom_integrations=True,
            priority_support=True,
            live_match_analysis=True,
        ),
        "target_audience": "Professional clubs, agencies, media companies",
        "call_to_action": "Everything you need to compete",
    },

    PlanTier.ENTERPRISE: {
        "pricing": PlanPricing(
            tier=PlanTier.ENTERPRISE,
            name="Enterprise",
            description="Custom solutions for elite clubs and organizations",
            price_monthly_eur=0,  # Custom pricing
            price_yearly_eur=0,  # Contact us
        ),
        "features": PlanFeatures(
            player_reports_per_month=999999,  # Unlimited
            leagues_access=999,  # All leagues + custom
            team_fit_analyses_per_month=999999,  # Unlimited
            api_requests_per_month=999999,  # Unlimited
            advanced_metrics=True,
            moneyball_valuation=True,
            pdf_exports=True,
            excel_exports=True,
            email_reports=True,
            api_access=True,
            webhook_support=True,
            custom_endpoints=True,
            multi_user_seats=999,  # Unlimited
            white_label_reports=True,
            custom_integrations=True,
            priority_support=True,
            dedicated_account_manager=True,
            live_match_analysis=True,
            real_time_alerts=True,
        ),
        "target_audience": "Elite clubs, major media companies, betting operators",
        "call_to_action": "Contact us for custom pricing",
        "contact_required": True,
    },
}


# =====================================================
# PRICING TABLE DATA
# =====================================================

PRICING_TABLE = {
    "features_comparison": [
        {
            "category": "Core Features",
            "features": [
                {
                    "name": "Player Reports per Month",
                    "free": "10",
                    "scout": "100",
                    "professional": "500",
                    "club": "Unlimited",
                    "enterprise": "Unlimited",
                },
                {
                    "name": "Leagues Access",
                    "free": "3 leagues",
                    "scout": "10 leagues",
                    "professional": "50+ leagues",
                    "club": "All leagues",
                    "enterprise": "All + Custom",
                },
                {
                    "name": "Team Fit Analysis",
                    "free": "❌",
                    "scout": "10/month",
                    "professional": "Unlimited",
                    "club": "Unlimited",
                    "enterprise": "Unlimited",
                },
                {
                    "name": "PDF Exports",
                    "free": "❌",
                    "scout": "✅",
                    "professional": "✅",
                    "club": "✅",
                    "enterprise": "✅",
                },
            ],
        },
        {
            "category": "Advanced Analytics",
            "features": [
                {
                    "name": "Expected Goals (xG)",
                    "free": "❌",
                    "scout": "❌",
                    "professional": "✅",
                    "club": "✅",
                    "enterprise": "✅",
                },
                {
                    "name": "Moneyball Valuation",
                    "free": "❌",
                    "scout": "❌",
                    "professional": "✅",
                    "club": "✅",
                    "enterprise": "✅",
                },
                {
                    "name": "Opta Performance Index",
                    "free": "Basic",
                    "scout": "✅",
                    "professional": "✅ Advanced",
                    "club": "✅ Advanced",
                    "enterprise": "✅ Custom",
                },
                {
                    "name": "Live Match Analysis",
                    "free": "❌",
                    "scout": "❌",
                    "professional": "❌",
                    "club": "✅",
                    "enterprise": "✅",
                },
            ],
        },
        {
            "category": "API & Integration",
            "features": [
                {
                    "name": "API Access",
                    "free": "❌",
                    "scout": "1K req/month",
                    "professional": "10K req/month",
                    "club": "100K req/month",
                    "enterprise": "Unlimited",
                },
                {
                    "name": "Webhooks",
                    "free": "❌",
                    "scout": "❌",
                    "professional": "❌",
                    "club": "✅",
                    "enterprise": "✅",
                },
                {
                    "name": "Custom Integrations",
                    "free": "❌",
                    "scout": "❌",
                    "professional": "❌",
                    "club": "✅",
                    "enterprise": "✅ Priority",
                },
            ],
        },
        {
            "category": "Team Features",
            "features": [
                {
                    "name": "User Seats",
                    "free": "1",
                    "scout": "1",
                    "professional": "1",
                    "club": "5",
                    "enterprise": "Unlimited",
                },
                {
                    "name": "White-Label Reports",
                    "free": "❌",
                    "scout": "❌",
                    "professional": "❌",
                    "club": "✅",
                    "enterprise": "✅",
                },
                {
                    "name": "Dedicated Support",
                    "free": "❌",
                    "scout": "❌",
                    "professional": "Priority",
                    "club": "Priority",
                    "enterprise": "Account Manager",
                },
            ],
        },
    ],
}


# =====================================================
# HELPER FUNCTIONS
# =====================================================

def get_plan(tier: PlanTier) -> dict:
    """Get complete plan information."""
    return PLANS.get(tier, PLANS[PlanTier.FREE])


def get_plan_features(tier: PlanTier) -> PlanFeatures:
    """Get features for a plan."""
    return PLANS[tier]["features"]


def get_plan_pricing(tier: PlanTier) -> PlanPricing:
    """Get pricing for a plan."""
    return PLANS[tier]["pricing"]


def can_access_feature(tier: PlanTier, feature: str) -> bool:
    """Check if a plan tier has access to a feature."""
    features = get_plan_features(tier)
    return getattr(features, feature, False)


def check_usage_limit(tier: PlanTier, usage_type: str, current_usage: int) -> Tuple[bool, int]:
    """
    Check if user is within usage limits.

    Args:
        tier: User's plan tier
        usage_type: Type of usage (e.g., 'player_reports_per_month')
        current_usage: Current usage count

    Returns:
        (allowed: bool, remaining: int)
    """
    features = get_plan_features(tier)
    limit = getattr(features, usage_type, 0)

    if limit == 999999:  # Unlimited
        return True, 999999

    allowed = current_usage < limit
    remaining = max(0, limit - current_usage)

    return allowed, remaining


def get_upgrade_recommendation(tier: PlanTier, blocked_feature: str = None) -> Optional[PlanTier]:
    """
    Recommend which plan to upgrade to based on blocked feature.

    Args:
        tier: Current plan tier
        blocked_feature: Feature that user tried to access but couldn't

    Returns:
        Recommended tier to upgrade to
    """
    tier_order = [PlanTier.FREE, PlanTier.SCOUT, PlanTier.PROFESSIONAL, PlanTier.CLUB, PlanTier.ENTERPRISE]

    current_index = tier_order.index(tier)

    # Find next tier that has the blocked feature
    for next_tier in tier_order[current_index + 1:]:
        if blocked_feature and can_access_feature(next_tier, blocked_feature):
            return next_tier

    # Default: recommend next tier
    if current_index < len(tier_order) - 1:
        return tier_order[current_index + 1]

    return None


# =====================================================
# MARKETING COPY
# =====================================================

MARKETING_HEADLINES = {
    "hero": "Professional Sports Analytics for Everyone",
    "subhero": "Get the insights used by top clubs, at a fraction of the cost. No PhD required.",
    "value_prop_1": "Find Hidden Talent Before Your Competitors",
    "value_prop_2": "Make Data-Driven Transfer Decisions",
    "value_prop_3": "Stop Overpaying for Players",
}

SOCIAL_PROOF = {
    "stats": [
        {"number": "50+", "label": "Leagues Covered"},
        {"number": "85%", "label": "Opta-Level Coverage"},
        {"number": "€29", "label": "Starting Price"},
        {"number": "3,000+", "label": "Happy Users"},
    ],
    "testimonials": [
        {
            "quote": "ScoutAI helped us find three players who became key starters. The Team Fit Analysis is incredible.",
            "author": "James Mitchell",
            "title": "Head Scout, League Two Club",
        },
        {
            "quote": "Finally, professional analytics I can actually afford. The Moneyball features paid for themselves in one signing.",
            "author": "Sarah Chen",
            "title": "Independent Agent",
        },
        {
            "quote": "Better than tools costing 10x more. The xG data alone is worth the subscription.",
            "author": "Mike Thompson",
            "title": "Sports Analyst",
        },
    ],
}


if __name__ == "__main__":
    # Demo usage
    print("="*60)
    print("SCOUTAI - PRODUCT CONFIGURATION")
    print("="*60)
    print()

    for tier in PlanTier:
        plan = get_plan(tier)
        pricing = plan["pricing"]
        features = plan["features"]

        print(f"\n{pricing.name.upper()} - €{pricing.price_monthly_eur}/month")
        print("-"*60)
        print(f"  Player Reports: {features.player_reports_per_month}")
        print(f"  Leagues: {features.leagues_access}")
        print(f"  Team Fit: {features.team_fit_analyses_per_month}")
        print(f"  API Requests: {features.api_requests_per_month}")
        print(f"  Advanced Metrics: {'✅' if features.advanced_metrics else '❌'}")
        print(f"  Moneyball: {'✅' if features.moneyball_valuation else '❌'}")

    print("\n" + "="*60)
    print("Ready to make money! 💰")
