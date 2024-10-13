import sys
from pathlib import Path
import scipy.stats as stats
import json
# Add the project directory to the sys.path
project_dir = str(Path(__file__).resolve().parents[1])
if project_dir not in sys.path:
    sys.path.append(project_dir)
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from ...mapping import OPTIONS_EXCHANGES
indices_list = ["SPX", "SPXW", "NDX", "VIX", "VVIX"]
from scipy.stats import norm



class UniversalOptionSnapshot:
    def __init__(self, results):
        self.break_even = [float(i['break_even_price']) if 'break_even_price' is not None and 'break_even_price' in i else None for i in results]
        self.implied_volatility = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in results] 
        self.open_interest = [float(i['open_interest']) if 'open_interest' in i else None for i in results]
        self.risk_free_rate=4.87
        
        day = [i['day'] if 'day' in i else 0 for i in results]
        self.volume = [float(i.get('volume',0)) for i in day]
        self.high = [float(i.get('high',0)) for i in day]
        self.low = [float(i.get('low',0)) for i in day]
        self.vwap = [float(i.get('vwap',0)) for i in day]
        self.open = [float(i.get('open',0)) for i in day]
        self.close = [float(i.get('close',0)) for i in day]
        self.change_percent= [round(float(i.get('change_percent',0))) for i in day]



        details = [i['details'] if 'details' in i else 0 for i in results]
        self.strike = [float(i['strike_price']) if 'strike_price' in i else None for i in details]
        self.expiry = [i['expiration_date'] if 'expiration_date' in i else None for i in details]
        # Convert the expiration dates into a pandas Series
        expiry_series = pd.Series(self.expiry)
        expiry_series = pd.to_datetime(expiry_series)

        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in details]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in details]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in details]

        greeks = [i.get('greeks') for i in results]
        self.theta = [round(float(i['theta']),4) if 'theta' in i else None for i in greeks]
        self.delta = [round(float(i['delta']),4) if 'delta' in i else None for i in greeks]
        self.gamma = [round(float(i['gamma']),4) if 'gamma' in i else None for i in greeks]
        self.vega = [round(float(i['vega']),4) if 'vega' in i else None for i in greeks]


        last_trade = [i['last_trade'] if i['last_trade'] is not None else None for i in results]
        self.sip_timestamp = [i['sip_timestamp'] if 'sip_timestamp' in i else None for i in last_trade]
        self.conditions = [i['conditions'] if 'conditions' in i else None for i in last_trade]
        self.conditions = [condition for sublist in self.conditions for condition in (sublist if isinstance(sublist, list) else [sublist])]
        self.trade_price = [float(i['price']) if 'price' in i else None for i in last_trade]
        self.trade_size = [float(i['size']) if 'size' in i else None for i in last_trade]
        self.exchange = [i['exchange'] if 'exchange' in i else None for i in last_trade]


        last_quote = [i['last_quote'] if i['last_quote'] is not None else None for i in results]
        self.ask = [float(i['ask']) if 'ask' in i and i['ask'] is not None else None for i in last_quote]
        self.bid = [float(i['bid']) if 'bid' in i and i['bid'] is not None else None for i in last_quote]
        self.bid_size = [float(i['bid_size']) if 'bid_size' in i and i['bid_size'] is not None else None for i in last_quote]
        self.ask_size = [float(i['ask_size']) if 'ask_size' in i and i['ask_size'] is not None else None for i in last_quote]
        self.midpoint = [float(i['midpoint']) if 'midpoint' in i and i['midpoint'] is not None else None for i in last_quote]



        underlying_asset = [i['underlying_asset'] if i['underlying_asset'] is not None else None for i in results]
        self.change_to_breakeven = [float(i['change_to_break_even']) if 'change_to_break_even' in i else None for i in underlying_asset]
        self.underlying_price = [float(i.get('price')) if i.get('price') is not None else None for i in underlying_asset]
        self.risk_free_rate = [self.risk_free_rate] * len(self.underlying_price)
        self.underlying_ticker = [i['ticker'] if 'ticker' in i else None for i in underlying_asset]
        today = pd.Timestamp(datetime.today())
        
        
        expiry_series = pd.to_datetime(self.expiry)

        # Today's date
        today = pd.to_datetime(datetime.now())

        # Calculate days to expiry for each date in the series
        self.days_to_expiry_series = (expiry_series - today).days
        self.time_value = [float(p) - float(s) + float(k) if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
        self.time_value = [round(item, 3) if item is not None else None for item in self.time_value]

        self.moneyness = [
            'Unknown' if u is None else (
                'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
                    'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
                )
            ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        ]

        self.liquidity_indicator = [float(a_size) + float(b_size) if a_size is not None and b_size is not None else None for a_size, b_size in zip(self.ask_size, self.bid_size)]
        self.liquidity_indicator = [round(item, 3) if item is not None else None for item in self.liquidity_indicator]

        self.spread = [float(a) - float(b) if a is not None and b is not None else None for a, b in zip(self.ask, self.bid)]
        self.intrinsic_value = [float(u) - float(s) if ct == 'call' and u is not None and s is not None and u > s else float(s) - float(u) if ct == 'put' and u is not None and s is not None and s > u else 0.0 for ct, u, s in zip(self.contract_type, self.underlying_price, self.strike)]
        self.intrinsic_value =[round(item, 3) if item is not None else None for item in self.intrinsic_value]
        self.extrinsic_value = [float(p) - float(iv) if p is not None and iv is not None else None for p, iv in zip(self.trade_price, self.intrinsic_value)]
        self.extrinsic_value =[round(item, 3) if item is not None else None for item in self.extrinsic_value]
        self.leverage_ratio = [float(d) / (float(s) / float(u)) if d is not None and s is not None and u is not None else None for d, s, u in zip(self.delta, self.strike, self.underlying_price)]
        self.leverage_ratio = [round(item, 3) if item is not None else None for item in self.leverage_ratio]
        self.spread_pct = [(float(a) - float(b)) / float(m) * 100.0 if a is not None and b is not None and m is not None and m != 0 else None for a, b, m in zip(self.ask, self.bid, self.midpoint)]

        self.spread_pct = [round(item, 3) if item is not None else None for item in self.spread_pct]
        self.return_on_risk = [float(p) / (float(s) - float(u)) if ct == 'call' and p is not None and s is not None and u is not None and s > u else float(p) / (float(u) - float(s)) if ct == 'put' and p is not None and s is not None and u is not None and s < u else 0.0 for ct, p, s, u in zip(self.contract_type, self.trade_price, self.strike, self.underlying_price)]
        self.return_on_risk = [round(item, 3) if item is not None else None for item in self.return_on_risk]
        self.option_velocity = [float(delta) / float(p) if delta is not None and p is not None else 0.0 for delta, p in zip(self.delta, self.trade_price)]
        self.option_velocity = [round(item, 3) if item is not None else None for item in self.option_velocity]
        self.gamma_risk = [float(g) * float(u) if g is not None and u is not None else None for g, u in zip(self.gamma, self.underlying_price)]
        self.gamma_risk =[round(item, 3) if item is not None else None for item in self.gamma_risk]
        self.theta_decay_rate = [float(t) / float(p) if t is not None and p is not None else None for t, p in zip(self.theta, self.trade_price)]
        self.theta_decay_rate = [round(item, 3) if item is not None else None for item in self.theta_decay_rate]
        self.vega_impact = [float(v) / float(p) if v is not None and p is not None else None for v, p in zip(self.vega, self.trade_price)]
        self.vega_impact =[round(item, 3) if item is not None else None for item in self.vega_impact]
        self.delta_to_theta_ratio = [float(d) / float(t) if d is not None and t is not None and t != 0 else None for d, t in zip(self.delta, self.theta)]
        self.delta_to_theta_ratio = [round(item, 3) if item is not None else None for item in self.delta_to_theta_ratio]

        # Option sensitivity score - curated - finished
        self.oss = [(float(delta) if delta is not None else 0) + (0.5 * float(gamma) if gamma is not None else 0) + (0.1 * float(vega) if vega is not None else 0) - (0.5 * float(theta) if theta is not None else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.oss = [round(item, 3) for item in self.oss]

        # Liquidity-theta ratio - curated - finished
        self.ltr = [liquidity / abs(theta) if liquidity and theta else None for liquidity, theta in zip(self.liquidity_indicator, self.theta)]

        # Risk-reward score - curated - finished
        self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.implied_volatility)]
        scaling_factor = 1e5  # Use a scaling factor to make the values more readable
        # Greeks-balance score - curated - finished
        self.gbs = [(abs(delta) if delta else 0) + (abs(gamma) if gamma else 0) - (abs(vega) if vega else 0) - (abs(theta) if theta else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.gbs = [round(item, 3) if item is not None else None for item in self.gbs]

        # Options profit potential: FINAL - finished
        self.opp = [moneyness_score * oss * ltr * rrs if moneyness_score and oss and ltr and rrs else None for moneyness_score, oss, ltr, rrs in zip([1 if m == 'ITM' else 0.5 if m == 'ATM' else 0.2 for m in self.moneyness], self.oss, self.ltr, self.rrs)]
        self.opp = [round(item, 3) if item is not None else None for item in self.opp]

        # Create a pandas series from implied volatility without dropping NaN values
        iv_series = pd.Series(self.implied_volatility)

        # Rank the series while leaving NaN values in place
        self.iv_percentile = [round(x, 2) if not pd.isna(x) else None for x in iv_series.rank(pct=True)]

        t_years = self.days_to_expiry_series / 365

        epsilon = 1e-10  # Small constant to avoid division by zero

        d1 = [
            (np.log(u / s) + (r + 0.5 * iv**2) * t) / (iv * np.sqrt(t))
            if u is not None and u > epsilon and s is not None and s > epsilon and r is not None and iv is not None and iv > epsilon and t > epsilon
            else None
            for u, s, r, iv, t in zip(self.underlying_price, self.strike, self.risk_free_rate, self.implied_volatility, t_years)
        ]

        d2 = [
            d1_val - iv * np.sqrt(t)
            if d1_val is not None and iv is not None and t is not None and iv > epsilon and t > epsilon
            else None
            for d1_val, iv, t in zip(d1, self.implied_volatility, t_years)]
        self.vanna = [
            (v * d1_val / iv) if v is not None and d1_val is not None and iv is not None and iv > epsilon else None
            for v, d1_val, iv in zip(self.vega, d1, self.implied_volatility)
        ]

        vanna_min = min([x for x in self.vanna if x is not None], default=0)
        vanna_max = max([x for x in self.vanna if x is not None], default=1)
        if vanna_max != vanna_min:
            self.vanna = [((x - vanna_min) / (vanna_max - vanna_min)) * scaling_factor if x is not None else None for x in self.vanna]



        self.vanna_vega = [
        (d * (v / u)) if d is not None and v is not None and u is not None and u > epsilon else None
        for d, v, u in zip(self.delta, self.vega, self.underlying_price)
    ]
        self.vanna_delta = [
            (-g * u * iv * np.sqrt(t)) if g is not None and u is not None and iv is not None and t is not None and u > epsilon and iv > epsilon and t > epsilon else None
            for g, u, iv, t in zip(self.gamma, self.underlying_price, self.implied_volatility, t_years)
        ]
        # Nd1_prime Calculation
        Nd1_prime = [norm.pdf(d) if d is not None else None for d in d1]

        # Color Calculation
        self.color = [
            -g * ((d1_val / (2 * t)) + (r / (iv * np.sqrt(t))))
            if g is not None and d1_val is not None and iv is not None and t is not None and iv > epsilon and t > epsilon
            else None
            for g, d1_val, iv, t, r in zip(self.gamma, d1, self.implied_volatility, t_years, self.risk_free_rate)
        ]

        # Charm Calculation
        self.charm = [
            -nd1p * ((2 * r * t - d2_val * iv * np.sqrt(t)) / (2 * t * iv * np.sqrt(t)))
            if nd1p is not None and d2_val is not None and iv is not None and t is not None and iv > epsilon and t > epsilon
            else None
            for nd1p, d2_val, iv, t, r in zip(Nd1_prime, d2, self.implied_volatility, t_years, self.risk_free_rate)
        ]


        self.veta = [
            -u * nd1p * np.sqrt(t) * (r + (d1_val * d2_val) / t)
            if u is not None and nd1p is not None and t is not None and d1_val is not None and d2_val is not None and t > epsilon
            else None
            for u, nd1p, t, d1_val, d2_val, r in zip(self.underlying_price, Nd1_prime, t_years, d1, d2, self.risk_free_rate)
        ]


        # Zomma Calculation
        self.zomma = [
            g * (d1_val * d2_val - 1) / iv
            if g is not None and d1_val is not None and d2_val is not None and iv is not None and iv > epsilon
            else None
            for g, d1_val, d2_val, iv in zip(self.gamma, d1, d2, self.implied_volatility)
        ]

        # Speed Calculation
        self.speed = [
            -g * ((d1_val / (u * iv * np.sqrt(t))) + 1) / u
            if g is not None and d1_val is not None and u is not None and iv is not None and t is not None and u > epsilon and iv > epsilon and t > epsilon
            else None
            for g, d1_val, u, iv, t in zip(self.gamma, d1, self.underlying_price, self.implied_volatility, t_years)
        ]

        # Ultima Calculation
        self.ultima = [
            -v * (d1_val * d2_val * (d1_val * d2_val - 1) + d1_val**2 + d2_val**2) / iv**2
            if v is not None and d1_val is not None and d2_val is not None and iv is not None and iv > epsilon
            else None
            for v, d1_val, d2_val, iv in zip(self.vega, d1, d2, self.implied_volatility)
        ]

        ultima_min = min([x for x in self.ultima if x is not None], default=0)
        ultima_max = max([x for x in self.ultima if x is not None], default=1)
        if ultima_max != ultima_min:
            self.ultima = [((x - ultima_min) / (ultima_max - ultima_min)) * scaling_factor if x is not None else None for x in self.ultima]

        self.vomma = [
            v * d1_val * d2_val / iv if v is not None and d1_val is not None and d2_val is not None and iv is not None and iv > epsilon
            else None
            for v, d1_val, d2_val, iv in zip(self.vega, d1, d2, self.implied_volatility)
        ]

        vomma_min = min([x for x in self.vomma if x is not None], default=0)
        vomma_max = max([x for x in self.vomma if x is not None], default=1)
        if vomma_max != vomma_min:
            self.vomma = [((x - vomma_min) / (vomma_max - vomma_min)) * scaling_factor if x is not None else None for x in self.vomma]


        self.epsilon = [
            -t * u * norm.cdf(d1_val)
            if t is not None and t > epsilon and u is not None and d1_val is not None
            else None
            for t, u, d1_val in zip(t_years, self.underlying_price, d1)
        ]

        self.volga = [
            (v * d1_val * d2_val / iv) if v is not None and d1_val is not None and d2_val is not None and iv is not None and iv > epsilon
            else None
            for v, d1_val, d2_val, iv in zip(self.vega, d1, d2, self.implied_volatility)
        ]

        volga_min = min([x for x in self.volga if x is not None], default=0)
        volga_max = max([x for x in self.volga if x is not None], default=1)
        if volga_max != volga_min:
            self.volga = [((x - volga_min) / (volga_max - volga_min)) * scaling_factor if x is not None else None for x in self.volga]



        self.vera = [
            (v * d2_val / iv) if v is not None and d2_val is not None and iv is not None and iv > epsilon
            else None
            for v, d2_val, iv in zip(self.vega, d2, self.implied_volatility)
        ]

        vera_min = min([x for x in self.vera if x is not None], default=0)
        vera_max = max([x for x in self.vera if x is not None], default=1)
        if vera_max != vera_min:
            self.vera = [(x - vera_min) / (vera_max - vera_min) if x is not None else None for x in self.vera]


        self.data_dict = {
            'strike': self.strike,
            'expiry': self.expiry,
            'dte': self.days_to_expiry_series,
            'time_value': self.time_value,
            'moneyness': self.moneyness,
            'liquidity_score': self.liquidity_indicator,
            'cp': self.contract_type,
            'change_ratio': self.change_percent,
            'exercise_style': self.exercise_style,
            'option_symbol': self.ticker,
            'theta': self.theta,
            'theta_decay_rate': self.theta_decay_rate,
            'delta': self.delta,
            'delta_theta_ratio': self.delta_to_theta_ratio,
            'gamma': self.gamma,
            'gamma_risk': self.gamma_risk,
            'vega': self.vega,
            'vega_impact': self.vega_impact,
            'timestamp': self.sip_timestamp,
            'oi': self.open_interest,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'intrinsic_value': self.intrinsic_value,
            'extrinsic_value': self.extrinsic_value,
            'leverage_ratio': self.leverage_ratio,
            'vwap': self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'trade_size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'spread': self.spread,
            'spread_pct': self.spread_pct,
            'iv': self.implied_volatility,
            'iv_percentile': self.iv_percentile,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'mid': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'underlying_price': self.underlying_price,
            'ticker': self.underlying_ticker,
            'return_on_risk': self.return_on_risk,
            'velocity': self.option_velocity,
            'sensitivity': self.oss,
            'opp': self.opp,
            'vanna': self.vanna,
            'vanna_delta': self.vanna_delta,
            'vanna_vega': self.vanna_vega,
            'vomma': self.vomma,
            'charm': self.charm,
            'veta': self.veta,
            'speed': self.speed,
            'zomma': self.zomma,
            'color': self.color,
            'ultima': self.ultima,
            'epsilon': self.epsilon,
            'volga': self.volga,
            'vera': self.vera
            
     
        }
        # At the end of your __init__ method, before creating the DataFrame, check the lengths of all lists
        for key, value in self.data_dict.items():
            print(f"{key} length: {len(value)}")
                # Create DataFrame from data_dict
        # Create DataFrame from data_dict
        self.df = pd.DataFrame(self.data_dict)

        # Calculate weighted Greeks by OI for calls and puts
        self.df['weighted_delta'] = self.df['delta'] * self.df['oi']
        self.df['weighted_gamma'] = self.df['gamma'] * self.df['oi']
        self.df['weighted_vega'] = self.df['vega'] * self.df['oi']
        self.df['weighted_theta'] = self.df['theta'] * self.df['oi']
        self.df['weighted_vanna'] = self.df['vanna'] * self.df['oi']
        self.df['weighted_charm'] = self.df['charm'] * self.df['oi']
        self.df['weighted_veta'] = self.df['veta'] * self.df['oi']
        self.df['weighted_speed'] = self.df['speed'] * self.df['oi']
        self.df['weighted_zomma'] = self.df['zomma'] * self.df['oi']
        self.df['weighted_color'] = self.df['color'] * self.df['oi']
        self.df['weighted_ultima'] = self.df['ultima'] * self.df['oi']

        self.df['log_returns'] = np.log(self.df['underlying_price'] / self.df['underlying_price'].shift(1))
        # Calculate rolling historical volatility over a window (e.g., 20 days)
        self.df['historical_volatility'] = self.df['log_returns'].rolling(window=20).std() * np.sqrt(252)  # Annualize

        # Calculate relative implied volatility
        self.df['relative_iv'] = self.df['iv'] / self.df['historical_volatility']
        # Introduce weighted_oi as a composite metric
        self.df['weighted_oi'] = (
            self.df['weighted_delta'] +
            self.df['weighted_gamma'] +
            self.df['weighted_vega'] +
            self.df['weighted_theta'] +
            self.df['weighted_vanna'] +
            self.df['weighted_charm'] +
            self.df['weighted_veta'] +
            self.df['weighted_speed'] +
            self.df['weighted_zomma'] +
            self.df['weighted_color'] +
            self.df['weighted_ultima']
        )

        # Calculate the relative position of the option's strike price to the current underlying price
        self.df['strike_distance'] = np.abs(self.df['strike'] - self.df['underlying_price'])

        # Adjust the momentum factor calculation
        self.df['momentum_factor'] = self.df['strike_distance'].apply(
        lambda x: 1 / x if x > 0 else np.inf
    )

        # Calculate momentum-adjusted Greeks using the momentum factor derived from strike distance
        self.df['momentum_delta'] = self.df['delta'] * self.df['momentum_factor']
        self.df['momentum_gamma'] = self.df['gamma'] * self.df['momentum_factor']
        self.df['momentum_vega'] = self.df['vega'] * self.df['momentum_factor']
        self.df['momentum_theta'] = self.df['theta'] * self.df['momentum_factor']
        self.df['momentum_vanna'] = self.df['vanna'] * self.df['momentum_factor']
        self.df['momentum_charm'] = self.df['charm'] * self.df['momentum_factor']
        self.df['momentum_veta'] = self.df['veta'] * self.df['momentum_factor']
        self.df['momentum_speed'] = self.df['speed'] * self.df['momentum_factor']
        # Normalize momentum_speed
        min_value = self.df['momentum_speed'].min()
        max_value = self.df['momentum_speed'].max()
        self.df['momentum_speed'] = (self.df['momentum_speed'] - min_value) / (max_value - min_value)
        self.df['momentum_zomma'] = self.df['zomma'] * self.df['momentum_factor']
        self.df['momentum_color'] = self.df['color'] * self.df['momentum_factor']
        self.df['momentum_ultima'] = self.df['ultima'] * self.df['momentum_factor']




        epsilon = 1e-6
        self.df['weighted_liquidity'] = (
            (self.df['bid_size'] + self.df['ask_size']) /
            (self.df['ask'] - self.df['bid'] + epsilon) * self.df['oi']
        )

        self.df['relative_iv'] = self.df['iv'] / self.df['vwap']  # Assuming vwap as a proxy for historical volatility
        contract_multiplier = 100
        self.df['gamma_exposure'] = self.df['gamma'] * self.df['oi'] * (self.df['underlying_price'] ** 2) * contract_multiplier
        

        # Define log returns
        self.df['returns'] = np.log(self.df['underlying_price'] / self.df['underlying_price'].shift(1))

        # Use log_returns in calculations
        self.df['historical_volatility'] = self.df['log_returns'].rolling(window=20).std() * np.sqrt(252)

        # Calculate skewness of returns
        self.df['returns_skewness'] = self.df['returns'].rolling(window=20).apply(stats.skew, raw=True)

        # Calculate skewness of implied volatility
        self.df['iv_skewness'] = self.df['iv'].rolling(window=20).apply(stats.skew, raw=True)


        # Separate DataFrames for calls and puts
        self.call_positioning = self.df[self.df['cp'] == 'call']
        self.put_positioning = self.df[self.df['cp'] == 'put']


        # Aggregate dealer positioning metrics for calls, incorporating volume and OI
        self.call_dealer_positioning = self.call_positioning.groupby('strike').agg({
            'weighted_delta': 'sum',
            'weighted_gamma': 'sum',
            'weighted_vega': 'sum',
            'weighted_theta': 'sum',
            'weighted_vanna': 'sum',
            'weighted_charm': 'sum',
            'weighted_veta': 'sum',
            'weighted_speed': 'sum',
            'weighted_zomma': 'sum',
            'weighted_color': 'sum',
            'weighted_ultima': 'sum',
            'weighted_oi': 'sum',
            'oi': 'sum',
            'vol': 'sum'
        }).reset_index()

        # Normalize by total open interest to get true positioning
        for column in ['weighted_delta', 'weighted_gamma', 'weighted_vega', 'weighted_theta', 'weighted_vanna',
                    'weighted_charm', 'weighted_veta', 'weighted_speed', 'weighted_zomma', 'weighted_color',
                    'weighted_ultima', 'weighted_oi']:
            self.call_dealer_positioning[column] = self.call_dealer_positioning[column] / self.call_dealer_positioning['oi']

        # Repeat the same for puts
        self.put_dealer_positioning = self.put_positioning.groupby('strike').agg({
            'weighted_delta': 'sum',
            'weighted_gamma': 'sum',
            'weighted_vega': 'sum',
            'weighted_theta': 'sum',
            'weighted_vanna': 'sum',
            'weighted_charm': 'sum',
            'weighted_veta': 'sum',
            'weighted_speed': 'sum',
            'weighted_zomma': 'sum',
            'weighted_color': 'sum',
            'weighted_ultima': 'sum',
            'weighted_oi': 'sum',
            'oi': 'sum',
            'vol': 'sum'
        }).reset_index()

        for column in ['weighted_delta', 'weighted_gamma', 'weighted_vega', 'weighted_theta', 'weighted_vanna',
                    'weighted_charm', 'weighted_veta', 'weighted_speed', 'weighted_zomma', 'weighted_color',
                    'weighted_ultima', 'weighted_oi']:
            self.put_dealer_positioning[column] = self.put_dealer_positioning[column] / self.put_dealer_positioning['oi']

    def save_conversations_to_jsonl(self, filename: str):
        """
        Save the options data as a JSONL file formatted for fine-tuning.

        :param filename: The name of the file to save the data to (e.g., 'options_data.jsonl').
        """
        conversations = []

        for index, row in self.df.iterrows():
            conversation = {
                "messages": [
                    {
                        "role": "system",
                        "content": "You are an assistant specialized in financial data analysis and options trading."
                    },
                    {
                        "role": "user",
                        "content": f"Can you analyze the following option data?\n\n"
                                   f"Strike: {row['strike']}, Expiry: {row['expiry']}, Contract Type: {row['cp']}, "
                                   f"Open Interest: {row['oi']}, Implied Volatility: {row['iv']}, Delta: {row['delta']}, "
                                   f"Gamma: {row['gamma']}, Theta: {row['theta']}, Vega: {row['vega']}, "
                                   f"Moneyness: {row['moneyness']}, Time Value: {row['time_value']}, "
                                   f"Intrinsic Value: {row['intrinsic_value']}, Extrinsic Value: {row['extrinsic_value']}."
                    },
                    {
                        "role": "assistant",
                        "content": f"The option is {row['moneyness']} with a strike price of {row['strike']} and "
                                   f"an expiration date of {row['expiry']}. The current implied volatility is "
                                   f"{row['iv']}, and the delta is {row['delta']}, indicating that the option's "
                                   f"price will move {row['delta'] * 100:.2f}% for every 1% change in the underlying asset's price."
                    }
                ]
            }
            conversations.append(conversation)

        # Save the conversations as a JSONL file
        with open(filename, 'w') as file:
            for conversation in conversations:
                file.write(json.dumps(conversation) + '\n')
    def get_call_dealer_positioning(self):
        """
        Method to get call dealer positioning as a DataFrame.
        """
        return self.call_dealer_positioning

    def get_put_dealer_positioning(self):
        """
        Method to get put dealer positioning as a DataFrame.
        """
        return self.put_dealer_positioning
    def __repr__(self) -> str:
        return f"UniversalOptionSnapshot(break_even={self.break_even}, \
                implied_volatility={self.implied_volatility},\
                open_interest ={self.open_interest}, \
                change={self.exchange}, \
                expiry={self.expiry}, \
                ticker={self.ticker} \
                contract_type={self.contract_type}, \
                exercise_style={self.exercise_style}, \
                theta={self.theta}, \
                delta={self.delta}, \
                gamma={self.gamma}, \
                vega={self.vega}, \
                sip_timestamp={self.sip_timestamp}, \
                conditions={self.conditions}, \
                trade_price={self.trade_price}, \
                trade_size={self.trade_size}, \
                exchange={self.exchange}, \
                ask={self.ask}, \
                bid={self.bid}, \
                bid_size={self.bid_size}, \
                ask_size={self.ask_size}, \
                midpoint={self.midpoint}, \
                change_to_breakeven={self.change_to_breakeven}, \
                underlying_price={self.underlying_price}, \
                underlying_ticker={self.underlying_ticker})"

    def __getitem__(self, index):
        return self.df[index]

    def __setitem__(self, index, value):
        self.df[index] = value

    def __iter__(self):
        # If df is a DataFrame, it's already iterable (over its column labels)
        # To iterate over rows, use itertuples or iterrows
        self.iter = self.df.itertuples()
        return self

    def __next__(self):
        # Just return the next value from the DataFrame iterator
        try:
            return next(self.iter)
        except StopIteration:
            # When there are no more rows, stop iteration
            raise StopIteration



class UniversalOptionSnapshot2:
    def __init__(self, results):

        session = [i['session'] if 'session' in i else 0 for i in results]


#         self.break_even = [float(i['break_even_price']) if 'break_even_price' is not None and 'break_even_price' in i else None for i in results]
#         self.implied_volatility = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in results] 
#         self.open_interest = [float(i['open_interest']) if 'open_interest' in i else None for i in results]

#         day = [i['day'] if 'day' in i else 0 for i in results]
#         self.volume = [float(i.get('volume',0)) for i in day]
#         self.high = [float(i.get('high',0)) for i in day]
#         self.low = [float(i.get('low',0)) for i in day]
#         self.vwap = [float(i.get('vwap',0)) for i in day]
#         self.open = [float(i.get('open',0)) for i in day]
#         self.close = [float(i.get('close',0)) for i in day]
#         self.change_percent= [round(float(i.get('change_percent',0))*100,2) for i in day]



#         details = [i['details'] for i in results]
#         self.strike = [float(i['strike_price']) if 'strike_price' in i else None for i in details]
#         self.expiry = [i['expiration_date'] if 'expiration_date' in i else None for i in details]
#         # Convert the expiration dates into a pandas Series
#         expiry_series = pd.Series(self.expiry)
#         expiry_series = pd.to_datetime(expiry_series)

#         self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in details]
#         self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in details]
#         self.ticker = [i['ticker'] if 'ticker' in i else None for i in details]

#         greeks = [i.get('greeks') for i in results]
#         self.theta = [round(float(i['theta']),4) if 'theta' in i else None for i in greeks]
#         self.delta = [round(float(i['delta']),4) if 'delta' in i else None for i in greeks]
#         self.gamma = [round(float(i['gamma']),4) if 'gamma' in i else None for i in greeks]
#         self.vega = [round(float(i['vega']),4) if 'vega' in i else None for i in greeks]


#         last_trade = [i['last_trade'] if i['last_trade'] is not None else None for i in results]
#         self.sip_timestamp = [i['sip_timestamp'] if 'sip_timestamp' in i else None for i in last_trade]
#         self.conditions = [i['conditions'] if 'conditions' in i else None for i in last_trade]
#         #self.conditions = [condition for sublist in self.conditions for condition in (sublist if isinstance(sublist, list) else [sublist])]
#         self.trade_price = [float(i['price']) if 'price' in i else None for i in last_trade]
#         self.trade_size = [float(i['size']) if 'size' in i else None for i in last_trade]
#         self.exchange = [i['exchange'] if 'exchange' in i else None for i in last_trade]
#         #self.exchange = [OPTIONS_EXCHANGES.get(i) for i in self.exchange]

#         last_quote = [i['last_quote'] if i['last_quote'] is not None else None for i in results]
#         self.ask = [float(i['ask']) if 'ask' in i and i['ask'] is not None else None for i in last_quote]
#         self.bid = [float(i['bid']) if 'bid' in i and i['bid'] is not None else None for i in last_quote]
#         self.bid_size = [float(i['bid_size']) if 'bid_size' in i and i['bid_size'] is not None else None for i in last_quote]
#         self.ask_size = [float(i['ask_size']) if 'ask_size' in i and i['ask_size'] is not None else None for i in last_quote]
#         self.midpoint = [float(i['midpoint']) if 'midpoint' in i and i['midpoint'] is not None else None for i in last_quote]



#         underlying_asset = [i['underlying_asset'] if i['underlying_asset'] is not None else None for i in results]
#         self.change_to_breakeven = [float(i['change_to_break_even']) if 'change_to_break_even' in i else None for i in underlying_asset]
#         self.underlying_price = [float(i.get('price')) if i.get('price') is not None else None for i in underlying_asset]

#         self.underlying_ticker = [i['ticker'] if 'ticker' in i else None for i in underlying_asset]
#         today = pd.Timestamp(datetime.today())
        
        
#         expiry_series = pd.to_datetime(self.expiry)

#         # Today's date
#         today = pd.to_datetime(datetime.now())

#         # Calculate days to expiry for each date in the series
#         self.days_to_expiry_series = (expiry_series - today).days
#         self.time_value = [float(p) - float(s) + float(k) if p and s and k else None for p, s, k in zip(self.trade_price, self.underlying_price, self.strike)]
#         self.time_value = [round(item, 3) if item is not None else None for item in self.time_value]

#         self.moneyness = [
#             'Unknown' if u is None else (
#                 'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
#                     'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
#                 )
#             ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
#         ]

#         self.liquidity_indicator = [float(a_size) + float(b_size) if a_size is not None and b_size is not None else None for a_size, b_size in zip(self.ask_size, self.bid_size)]
#         self.liquidity_indicator = [round(item, 3) if item is not None else None for item in self.liquidity_indicator]

#         self.spread = [float(a) - float(b) if a is not None and b is not None else None for a, b in zip(self.ask, self.bid)]
#         self.intrinsic_value = [float(u) - float(s) if ct == 'call' and u is not None and s is not None and u > s else float(s) - float(u) if ct == 'put' and u is not None and s is not None and s > u else 0.0 for ct, u, s in zip(self.contract_type, self.underlying_price, self.strike)]
#         self.intrinsic_value =[round(item, 3) if item is not None else None for item in self.intrinsic_value]
#         self.extrinsic_value = [float(p) - float(iv) if p is not None and iv is not None else None for p, iv in zip(self.trade_price, self.intrinsic_value)]
#         self.extrinsic_value =[round(item, 3) if item is not None else None for item in self.extrinsic_value]
#         self.leverage_ratio = [float(d) / (float(s) / float(u)) if d is not None and s is not None and u is not None else None for d, s, u in zip(self.delta, self.strike, self.underlying_price)]
#         self.leverage_ratio = [round(item, 3) if item is not None else None for item in self.leverage_ratio]
#         self.spread_pct = [(float(a) - float(b)) / float(m) * 100.0 if a is not None and b is not None and m is not None and m != 0 else None for a, b, m in zip(self.ask, self.bid, self.midpoint)]

#         self.spread_pct = [round(item, 3) if item is not None else None for item in self.spread_pct]
#         self.return_on_risk = [float(p) / (float(s) - float(u)) if ct == 'call' and p is not None and s is not None and u is not None and s > u else float(p) / (float(u) - float(s)) if ct == 'put' and p is not None and s is not None and u is not None and s < u else 0.0 for ct, p, s, u in zip(self.contract_type, self.trade_price, self.strike, self.underlying_price)]
#         self.return_on_risk = [round(item, 3) if item is not None else None for item in self.return_on_risk]
#         self.option_velocity = [float(delta) / float(p) if delta is not None and p is not None else 0.0 for delta, p in zip(self.delta, self.trade_price)]
#         self.option_velocity =[round(item, 3) if item is not None else None for item in self.option_velocity]
#         self.gamma_risk = [float(g) * float(u) if g is not None and u is not None else None for g, u in zip(self.gamma, self.underlying_price)]
#         self.gamma_risk =[round(item, 3) if item is not None else None for item in self.gamma_risk]
#         self.theta_decay_rate = [float(t) / float(p) if t is not None and p is not None else None for t, p in zip(self.theta, self.trade_price)]
#         self.theta_decay_rate = [round(item, 3) if item is not None else None for item in self.theta_decay_rate]
#         self.vega_impact = [float(v) / float(p) if v is not None and p is not None else None for v, p in zip(self.vega, self.trade_price)]
#         self.vega_impact =[round(item, 3) if item is not None else None for item in self.vega_impact]
#         self.delta_to_theta_ratio = [float(d) / float(t) if d is not None and t is not None and t != 0 else None for d, t in zip(self.delta, self.theta)]
#         self.delta_to_theta_ratio = [round(item, 3) if item is not None else None for item in self.delta_to_theta_ratio]
#         #option_sensitivity score - curated - finished
#         self.oss = [(float(delta) if delta is not None else 0) + (0.5 * float(gamma) if gamma is not None else 0) + (0.1 * float(vega) if vega is not None else 0) - (0.5 * float(theta) if theta is not None else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
#         self.oss = [round(item, 3) for item in self.oss]
#         #liquidity-theta ratio - curated - finished
#         self.ltr = [
#             liquidity / abs(theta) if liquidity and theta and theta != 0 else None
#             for liquidity, theta in zip(self.liquidity_indicator, self.theta)
#         ]
#         #risk-reward score - curated - finished
#         self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.implied_volatility)]
#         #greeks-balance score - curated - finished
#         self.gbs = [(abs(delta) if delta else 0) + (abs(gamma) if gamma else 0) - (abs(vega) if vega else 0) - (abs(theta) if theta else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
#         self.gbs = [round(item, 3) if item is not None else None for item in self.gbs]
#         #options profit potential: FINAL - finished
#         self.opp = [moneyness_score*oss*ltr*rrs if moneyness_score and oss and ltr and rrs else None for moneyness_score, oss, ltr, rrs in zip([1 if m == 'ITM' else 0.5 if m == 'ATM' else 0.2 for m in self.moneyness], self.oss, self.ltr, self.rrs)]
#         self.opp = [round(item, 3) if item is not None else None for item in self.opp]



                


















#         self.data_dict = {
#             'strike': self.strike,
#             'expiry': self.expiry,
#             'dte': self.days_to_expiry_series,
#             'time_value': self.time_value,
#             'moneyness': self.moneyness,
#             'liquidity_score': self.liquidity_indicator,
#             "cp": self.contract_type,
#             "change_ratio": self.change_percent,
#             'exercise_style': self.exercise_style,
#             'option_symbol': self.ticker,
#             'theta': self.theta,
#             'theta_decay_rate': self.theta_decay_rate,
#             'delta': self.delta,
#             'delta_theta_ratio': self.delta_to_theta_ratio,
#             'gamma': self.gamma,
#             'gamma_risk': self.gamma_risk,
#             'vega': self.vega,
#             'vega_impact': self.vega_impact,
#             'timestamp': self.sip_timestamp,
#             'oi': self.open_interest,
#             'open': self.open,
#             'high': self.high,
#             'low': self.low,
#             'close': self.close,
#             'intrinstic_value': self.intrinsic_value,
#             'extrinsic_value': self.extrinsic_value,
#             'leverage_ratio': self.leverage_ratio,
#             'vwap':self.vwap,
#             'conditions': self.conditions,
#             'price': self.trade_price,
#             'trade_size': self.trade_size,
#             'exchange': self.exchange,
#             'ask': self.ask,
#             'bid': self.bid,
#             'spread': self.spread,
#             'spread_pct': self.spread_pct,
#             'iv': self.implied_volatility,
#             'bid_size': self.bid_size,
#             'ask_size': self.ask_size,
#             'vol': self.volume,
#             'mid': self.midpoint,
#             'change_to_breakeven': self.change_to_breakeven,
#             'underlying_price': self.underlying_price,
#             'ticker': self.underlying_ticker,
#             'return_on_risk': self.return_on_risk,
#             'velocity': self.option_velocity,
#             'sensitivity': self.oss,
#             'greeks_balance': self.gbs,
#             'opp': self.opp
            
#         }


#         # Create DataFrame from data_dict
#         self.df = pd.DataFrame(self.data_dict)
#     def __repr__(self) -> str:
#         return f"UniversalOptionSnapshot(break_even={self.break_even}, \
#                 implied_volatility={self.implied_volatility},\
#                 open_interest ={self.open_interest}, \
#                 change={self.exchange}, \
#                 expiry={self.expiry}, \
#                 ticker={self.ticker} \
#                 contract_type={self.contract_type}, \
#                 exercise_style={self.exercise_style}, \
#                 theta={self.theta}, \
#                 delta={self.delta}, \
#                 gamma={self.gamma}, \
#                 vega={self.vega}, \
#                 sip_timestamp={self.sip_timestamp}, \
#                 conditions={self.conditions}, \
#                 trade_price={self.trade_price}, \
#                 trade_size={self.trade_size}, \
#                 exchange={self.exchange}, \
#                 ask={self.ask}, \
#                 bid={self.bid}, \
#                 bid_size={self.bid_size}, \
#                 ask_size={self.ask_size}, \
#                 midpoint={self.midpoint}, \
#                 change_to_breakeven={self.change_to_breakeven}, \
#                 underlying_price={self.underlying_price}, \
#                 underlying_ticker={self.underlying_ticker})"
    
#     def __getitem__(self, index):
#         return self.df[index]

#     def __setitem__(self, index, value):
#         self.df[index] = value
#     def __iter__(self):
#         # If df is a DataFrame, it's already iterable (over its column labels)
#         # To iterate over rows, use itertuples or iterrows
#         self.iter = self.df.itertuples()
#         return self

#     def __next__(self):
#         # Just return the next value from the DataFrame iterator
#         try:
#             return next(self.iter)
#         except StopIteration:
#             # When there are no more rows, stop iteration
#             raise StopIteration
        




class SPXSNAPSHOT:
    def __init__(self, results):
        self.break_even = [float(i['break_even_price']) if 'break_even_price' is not None and 'break_even_price' in i else None for i in results]
        self.implied_volatility = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in results] 
        self.open_interest = [float(i['open_interest']) if 'open_interest' in i else None for i in results]
        
        
        day = [i['day'] if 'day' in i else 0 for i in results]
        self.volume = [float(i.get('volume',0)) for i in day]
        self.high = [float(i.get('high',0)) for i in day]
        self.low = [float(i.get('low',0)) for i in day]
        self.vwap = [float(i.get('vwap',0)) for i in day]
        self.open = [float(i.get('open',0)) for i in day]
        self.close = [float(i.get('close',0)) for i in day]
        self.change_percent= [round(float(i.get('change_percent',0))) for i in day]



        details = [i['details'] if 'details' in i else 0 for i in results]
        self.strike = [float(i['strike_price']) if 'strike_price' in i else None for i in details]
        self.expiry = [i['expiration_date'] if 'expiration_date' in i else None for i in details]
        # Convert the expiration dates into a pandas Series
        expiry_series = pd.Series(self.expiry)
        expiry_series = pd.to_datetime(expiry_series)

        self.contract_type = [i['contract_type'] if 'contract_type' in i else None for i in details]
        self.exercise_style = [i['exercise_style'] if 'exercise_style' in i else None for i in details]
        self.ticker = [i['ticker'] if 'ticker' in i else None for i in details]

        greeks = [i.get('greeks') for i in results]
        self.theta = [round(float(i['theta']),4) if 'theta' in i else None for i in greeks]
        self.delta = [round(float(i['delta']),4) if 'delta' in i else None for i in greeks]
        self.gamma = [round(float(i['gamma']),4) if 'gamma' in i else None for i in greeks]
        self.vega = [round(float(i['vega']),4) if 'vega' in i else None for i in greeks]


        last_trade = [i['last_trade'] if i['last_trade'] is not None else None for i in results]
        self.sip_timestamp = [i['sip_timestamp'] if 'sip_timestamp' in i else None for i in last_trade]
        self.conditions = [i['conditions'] if 'conditions' in i else None for i in last_trade]
        self.conditions = [condition for sublist in self.conditions for condition in (sublist if isinstance(sublist, list) else [sublist])]
        self.trade_price = [float(i['price']) if 'price' in i else None for i in last_trade]
        self.trade_size = [float(i['size']) if 'size' in i else None for i in last_trade]
        self.exchange = [i['exchange'] if 'exchange' in i else None for i in last_trade]


        last_quote = [i['last_quote'] if i['last_quote'] is not None else None for i in results]
        self.ask = [float(i['ask']) if 'ask' in i and i['ask'] is not None else None for i in last_quote]
        self.bid = [float(i['bid']) if 'bid' in i and i['bid'] is not None else None for i in last_quote]
        self.bid_size = [float(i['bid_size']) if 'bid_size' in i and i['bid_size'] is not None else None for i in last_quote]
        self.ask_size = [float(i['ask_size']) if 'ask_size' in i and i['ask_size'] is not None else None for i in last_quote]
        self.midpoint = [float(i['midpoint']) if 'midpoint' in i and i['midpoint'] is not None else None for i in last_quote]



        underlying_asset = [i['underlying_asset'] if i['underlying_asset'] is not None else None for i in results]
        self.change_to_breakeven = [float(i['change_to_break_even']) if 'change_to_break_even' in i else None for i in underlying_asset]
        self.underlying_price = [float(i.get('price')) if i.get('price') is not None else None for i in underlying_asset]

        self.risk_free_rate = [self.risk_free_rate] * len(self.underlying_price)
        self.underlying_ticker = [i['ticker'] if 'ticker' in i else None for i in underlying_asset]

        
        expiry_series = pd.to_datetime(self.expiry)

        # Today's date
        today = pd.to_datetime(datetime.now())

  
        self.data_dict = {
            'strike': self.strike,
            'expiry': self.expiry,
            'cp': self.contract_type,
            'change_ratio': self.change_percent,
            'exercise_style': self.exercise_style,
            'option_symbol': self.ticker,
            'theta': self.theta,
            'delta': self.delta,
            'gamma': self.gamma,
            'vega': self.vega,
            'timestamp': self.sip_timestamp,
            'oi': self.open_interest,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'vwap': self.vwap,
            'conditions': self.conditions,
            'price': self.trade_price,
            'trade_size': self.trade_size,
            'exchange': self.exchange,
            'ask': self.ask,
            'bid': self.bid,
            'iv': self.implied_volatility,
            'bid_size': self.bid_size,
            'ask_size': self.ask_size,
            'vol': self.volume,
            'mid': self.midpoint,
            'change_to_breakeven': self.change_to_breakeven,
            'underlying_price': self.underlying_price,
            'ticker': self.underlying_ticker,
        }

        self.df = pd.DataFrame(self.data_dict)



class SpxSnapshot:
    def __init__(self, data):
        self.data=data
        self.session = [i.get('session', {}) if i is not None else {} for i in self.data]
        self.change = [
            float(i.get("change")) if isinstance(i.get("change"), (int, float)) else None
            for i in self.data
        ]
        self.risk_free_rate=3.79
        self.ticker = [i.get('ticker', {}) if i is not None else {} for i in self.data]
        self.name = [i.get('name', {}) if i is not None else {} for i in self.data]
        self.change_percent = [ float(i.get("change_percent")) if isinstance(i.get("change_percent"), (int, float)) else None for i in self.session ]
        self.close = [ float(i.get("close")) if isinstance(i.get("close"), (int, float)) else None for i in self.session ]
        self.early_trading_change = [ float(i.get("early_trading_change")) if isinstance(i.get("early_trading_change"), (int, float)) else None for i in self.session ]
        self.early_trading_change_percent = [ float(i.get("early_trading_change_percent")) if isinstance(i.get("early_trading_change_percent"), (int, float)) else None for i in self.session ]
        self.high = [ float(i.get("high")) if isinstance(i.get("high"), (int, float)) else None for i in self.session ]
        self.late_trading_change = [ float(i.get("late_trading_change")) if isinstance(i.get("late_trading_change"), (int, float)) else None for i in self.session ]
        self.late_trading_change_percent = [ float(i.get("late_trading_change_percent")) if isinstance(i.get("late_trading_change_percent"), (int, float)) else None for i in self.session ]
        self.low = [ float(i.get("low")) if isinstance(i.get("low"), (int, float)) else None for i in self.session ]
        self.open = [ float(i.get("open")) if isinstance(i.get("open"), (int, float)) else None for i in self.session ]
        self.previous_close = [ float(i.get("previous_close")) if isinstance(i.get("previous_close"), (int, float)) else None for i in self.session ]
        self.volume = [ float(i.get("volume")) if isinstance(i.get("volume"), (int, float)) else None for i in self.session ]

        self.details = [i.get('details', {}) if i is not None else {} for i in self.data]
        self.contract_type = [i.get("contract_type", {}) if i is not None else {} for i in self.details]
        self.exercise_style = [i.get("exercise_style", {}) if i is not None else {} for i in self.details]
        self.expiry = [i.get("expiration_date", {}) if i is not None else {} for i in self.details]
        self.shares_per_contract = [i.get("shares_per_contract", {}) if i is not None else {} for i in self.details]
        self.strike = [i.get("strike_price", {}) if i is not None else {} for i in self.details]



        self.greeks = [i.get('greeks') if isinstance(i, dict) and i is not None else {} for i in self.data]
        print(self.greeks)
        self.delta = [ round(float(i.get('delta')) * 100, 2) if isinstance(i.get('delta'), (int, float)) else None for i in self.greeks ]
        self.gamma = [ round(float(i.get('gamma')) * 100, 2) if isinstance(i.get('gamma'), (int, float)) else None for i in self.greeks ]
        self.theta = [ round(float(i.get('theta')) * 100, 2) if isinstance(i.get('theta'), (int, float)) else None for i in self.greeks ]
        self.vega = [ round(float(i.get('vega')) * 100, 2) if isinstance(i.get('vega'), (int, float)) else None for i in self.greeks ]




        self.last_quote = [i.get('last_quote', {}) if isinstance(i, dict) else {} for i in self.data]
        self.ask = [ float(i.get("ask")) if isinstance(i.get("ask"), (int, float)) else None for i in self.last_quote ]
        self.ask_exchange = [ i.get("ask_exchange") if isinstance(i.get("ask_exchange"), (int, float)) else None for i in self.last_quote ]
        self.ask_size = [ float(i.get("ask_size")) if isinstance(i.get("ask_size"), (int, float)) else None for i in self.last_quote ]
        self.bid = [ float(i.get("bid")) if isinstance(i.get("bid"), (int, float)) else None for i in self.last_quote ]
        self.bid_exchange = [ i.get("bid_exchange") if isinstance(i.get("bid_exchange"), (int, float)) else None for i in self.last_quote ]
        self.bid_size = [ float(i.get("bid_size")) if isinstance(i.get("bid_size"), (int, float)) else None for i in self.last_quote ]
        self.midpoint = [ float(i.get("midpoint")) if isinstance(i.get("midpoint"), (int, float)) else None for i in self.last_quote ]

        


        
        self.last_trade = [i.get('last_trade', {}) if isinstance(i, dict) else {} for i in self.data]
        self.conditions = [
            i.get('conditions')[0] if i.get('conditions') and isinstance(i.get('conditions'), list) else None
            for i in self.last_trade
        ]
        self.last_trade_price = [
            float(i.get("price")) if isinstance(i.get("price"), (int, float)) else None
            for i in self.last_trade
        ]
        self.last_trade_size = [
            float(i.get("size")) if isinstance(i.get("size"), (int, float)) else None
            for i in self.last_trade
        ]

        # Fixing the 'underlying_asset' section
        self.underlying_asset = [i.get('underlying_asset', {}) if isinstance(i, dict) else {} for i in self.data]
        self.last_trade_timestamp = [
       int(i.get("sip_timestamp")) if isinstance(i.get("sip_timestamp"), (int, float, str)) else None
    for i in self.last_trade
    ]
        self.underlying_price = [
            float(i.get("price")) if isinstance(i.get("price"), (int, float)) else None
            for i in self.underlying_asset
        ]
        self.risk_free_rate = [self.risk_free_rate] * len(self.underlying_price)
        self.underlying_symbol= [i.get("ticker", {}).replace('I:', '') for i in self.underlying_asset]

        
        # Safely parse the implied_volatility values, ensuring they are numbers self.iv = [ round(float(i.get('implied_volatility')) * 100, 2) if isinstance(i.get('implied_volatility'), (int, float)) else None for i in self.data ]
        # Safely parse the implied_volatility values, ensuring they are numbers
        self.oi = [ i.get('open_interest') if isinstance(i.get('open_interest'), (int, float)) else None for i in self.data]
        self.iv = [float(i['implied_volatility']) if 'implied_volatility' in i else None for i in self.data] 
        
        
        
        
        
        today = pd.Timestamp(datetime.today())
        
        
        expiry_series = pd.to_datetime(self.expiry)

        # Today's date
        today = pd.to_datetime(datetime.now())

        # Calculate days to expiry for each date in the series
        self.days_to_expiry_series = (expiry_series - today).days
        self.time_value = [float(p) - float(s) + float(k) if p and s and k else None for p, s, k in zip(self.last_trade_price, self.underlying_price, self.strike)]
        self.time_value = [round(item, 3) if item is not None else None for item in self.time_value]

        self.moneyness = [
            'Unknown' if u is None else (
                'ITM' if (ct == 'call' and s < u) or (ct == 'put' and s > u) else (
                    'OTM' if (ct == 'call' and s > u) or (ct == 'put' and s < u) else 'ATM'
                )
            ) for ct, s, u in zip(self.contract_type, self.strike, self.underlying_price)
        ]

        self.liquidity_indicator = [float(a_size) + float(b_size) if a_size is not None and b_size is not None else None for a_size, b_size in zip(self.ask_size, self.bid_size)]
        self.liquidity_indicator = [round(item, 3) if item is not None else None for item in self.liquidity_indicator]

        self.spread = [float(a) - float(b) if a is not None and b is not None else None for a, b in zip(self.ask, self.bid)]
        self.intrinsic_value = [float(u) - float(s) if ct == 'call' and u is not None and s is not None and u > s else float(s) - float(u) if ct == 'put' and u is not None and s is not None and s > u else 0.0 for ct, u, s in zip(self.contract_type, self.underlying_price, self.strike)]
        self.intrinsic_value =[round(item, 3) if item is not None else None for item in self.intrinsic_value]
        self.extrinsic_value = [float(p) - float(iv) if p is not None and iv is not None else None for p, iv in zip(self.last_trade_price, self.intrinsic_value)]
        self.extrinsic_value =[round(item, 3) if item is not None else None for item in self.extrinsic_value]
        self.leverage_ratio = [float(d) / (float(s) / float(u)) if d is not None and s is not None and u is not None else None for d, s, u in zip(self.delta, self.strike, self.underlying_price)]
        self.leverage_ratio = [round(item, 3) if item is not None else None for item in self.leverage_ratio]
        self.spread_pct = [(float(a) - float(b)) / float(m) * 100.0 if a is not None and b is not None and m is not None and m != 0 else None for a, b, m in zip(self.ask, self.bid, self.midpoint)]

        self.spread_pct = [round(item, 3) if item is not None else None for item in self.spread_pct]
        self.return_on_risk = [float(p) / (float(s) - float(u)) if ct == 'call' and p is not None and s is not None and u is not None and s > u else float(p) / (float(u) - float(s)) if ct == 'put' and p is not None and s is not None and u is not None and s < u else 0.0 for ct, p, s, u in zip(self.contract_type, self.last_trade_price, self.strike, self.underlying_price)]
        self.return_on_risk = [round(item, 3) if item is not None else None for item in self.return_on_risk]
        self.option_velocity = [float(delta) / float(p) if delta is not None and p is not None else 0.0 for delta, p in zip(self.delta, self.last_trade_price)]
        self.option_velocity = [round(item, 3) if item is not None else None for item in self.option_velocity]
        self.gamma_risk = [float(g) * float(u) if g is not None and u is not None else None for g, u in zip(self.gamma, self.underlying_price)]
        self.gamma_risk =[round(item, 3) if item is not None else None for item in self.gamma_risk]
        self.theta_decay_rate = [float(t) / float(p) if t is not None and p is not None else None for t, p in zip(self.theta, self.last_trade_price)]
        self.theta_decay_rate = [round(item, 3) if item is not None else None for item in self.theta_decay_rate]
        self.vega_impact = [float(v) / float(p) if v is not None and p is not None else None for v, p in zip(self.vega, self.last_trade_price)]
        self.vega_impact =[round(item, 3) if item is not None else None for item in self.vega_impact]
        self.delta_to_theta_ratio = [float(d) / float(t) if d is not None and t is not None and t != 0 else None for d, t in zip(self.delta, self.theta)]
        self.delta_to_theta_ratio = [round(item, 3) if item is not None else None for item in self.delta_to_theta_ratio]


        # Liquidity-theta ratio - curated - finished
        self.ltr = [liquidity / abs(theta) if liquidity and theta else None for liquidity, theta in zip(self.liquidity_indicator, self.theta)]

        # Risk-reward score - curated - finished
        self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.iv)]
        scaling_factor = 1e5  # Use a scaling factor to make the values more readable

        
        
        
        
        
        
        # Option sensitivity score - curated - finished
        self.oss = [(float(delta) if delta is not None else 0) + (0.5 * float(gamma) if gamma is not None else 0) + (0.1 * float(vega) if vega is not None else 0) - (0.5 * float(theta) if theta is not None else 0) for delta, gamma, vega, theta in zip(self.delta, self.gamma, self.vega, self.theta)]
        self.oss = [round(item, 3) for item in self.oss]

      

        # Risk-reward score - curated - finished
        self.rrs = [(intrinsic + extrinsic) / (iv + 1e-4) if intrinsic and extrinsic and iv else None for intrinsic, extrinsic, iv in zip(self.intrinsic_value, self.extrinsic_value, self.iv)]
        scaling_factor = 1e5  # Use a scaling factor to make the values more readable
        # Greeks-balance score - curated - finished

        # Options profit potential: FINAL - finished
        self.opp = [moneyness_score * oss * ltr * rrs if moneyness_score and oss and ltr and rrs else None for moneyness_score, oss, ltr, rrs in zip([1 if m == 'ITM' else 0.5 if m == 'ATM' else 0.2 for m in self.moneyness], self.oss, self.ltr, self.rrs)]
        self.opp = [round(item, 3) if item is not None else None for item in self.opp]

        # Create a pandas series from implied volatility without dropping NaN values
        iv_series = pd.Series(self.iv)

        # Rank the series while leaving NaN values in place
        self.iv_percentile = [round(x, 2) if not pd.isna(x) else None for x in iv_series.rank(pct=True)]

        t_years = self.days_to_expiry_series / 365

        # Calculate d1 and d2
        d1 = [
            (np.log(u / s) + (r + 0.5 * iv**2) * t) / (iv * np.sqrt(t))
            if u is not None and u > 0 and s is not None and s > 0 and r is not None and iv is not None and iv > 0 and t > 0
            else None
            for u, s, r, iv, t in zip(
                self.underlying_price, self.strike, self.risk_free_rate, self.iv, t_years
            )
        ]

        d2 = [
            d1_val - iv * np.sqrt(t)
            if d1_val and iv and t and iv > 0 and t > 0
            else None
            for d1_val, iv, t in zip(d1, self.iv, t_years)
        ]
        # Vanna Calculation
        self.vanna = [
            (v * d1_val / iv) if v and d1_val and iv and iv > 0 else None
            for v, d1_val, iv in zip(self.vega, d1, self.iv)
        ]

        # Normalize Vanna with scaling
        vanna_min = min([x for x in self.vanna if x is not None])
        vanna_max = max([x for x in self.vanna if x is not None])
        self.vanna = [((x - vanna_min) / (vanna_max - vanna_min)) * scaling_factor if x is not None else None for x in self.vanna]


        # Vanna_Vega Calculation (Note: This is not a standard Greek and may need verification)
        self.vanna_vega = [
            (d * (v / u))
            if d is not None and v is not None and u is not None and u > 0
            else None
            for d, v, u in zip(self.delta, self.vega, self.underlying_price)
        ]

        # Vanna_Delta Calculation
        self.vanna_delta = [
            (-g * u * iv * np.sqrt(t))
            if g and u and iv and t and u > 0 and iv > 0 and t > 0
            else None
            for g, u, iv, t in zip(self.gamma, self.underlying_price, self.iv, t_years)
        ]

        # Nd1_prime Calculation
        Nd1_prime = [norm.pdf(d) if d is not None else None for d in d1]

        # Color Calculation
        self.color = [
            -g * ((d1_val / (2 * t)) + (r / (iv * np.sqrt(t))))
            if g and d1_val and iv and t and iv > 0 and t > 0
            else None
            for g, d1_val, iv, t, r in zip(self.gamma, d1, self.iv, t_years, self.risk_free_rate)
        ]

        # Charm Calculation
        self.charm = [
            -nd1p
            * (
                (2 * r * t - d2_val * iv * np.sqrt(t))
                / (2 * t * iv * np.sqrt(t))
            )
            if nd1p and d2_val and iv and t and iv > 0 and t > 0
            else None
            for nd1p, d2_val, iv, t, r in zip(Nd1_prime, d2, self.iv, t_years, self.risk_free_rate)
        ]

        # Veta Calculation
        self.veta = [
            -u * nd1p * np.sqrt(t) * (r + (d1_val * d2_val) / t)
            if u and nd1p and t and d1_val and d2_val and t > 0
            else None
            for u, nd1p, t, d1_val, d2_val, r in zip(
                self.underlying_price, Nd1_prime, t_years, d1, d2, self.risk_free_rate
            )
        ]

        # Zomma Calculation
        self.zomma = [
            g * (d1_val * d2_val - 1) / iv
            if g and d1_val and d2_val and iv and iv > 0
            else None
            for g, d1_val, d2_val, iv in zip(self.gamma, d1, d2, self.iv)
        ]

        # Speed Calculation
        self.speed = [
            -g * ((d1_val / (u * iv * np.sqrt(t))) + 1) / u
            if g and d1_val and u and iv and t and u > 0 and iv > 0 and t > 0
            else None
            for g, d1_val, u, iv, t in zip(
                self.gamma, d1, self.underlying_price, self.iv, t_years
            )
        ]
        # Ultima Calculation
        self.ultima = [
            -v * (d1_val * d2_val * (d1_val * d2_val - 1) + d1_val**2 + d2_val**2) / iv**2
            if v and d1_val and d2_val and iv and iv > 0 else None
            for v, d1_val, d2_val, iv in zip(self.vega, d1, d2, self.iv)
        ]

        # Normalize Ultima with scaling
        ultima_min = min([x for x in self.ultima if x is not None])
        ultima_max = max([x for x in self.ultima if x is not None])
        self.ultima = [((x - ultima_min) / (ultima_max - ultima_min)) * scaling_factor if x is not None else None for x in self.ultima]

        # Vomma Calculation
        self.vomma = [
            v * d1_val * d2_val / iv if v and d1_val and d2_val and iv and iv > 0 else None
            for v, d1_val, d2_val, iv in zip(self.vega, d1, d2, self.iv)
        ]

        # Normalize Vomma with scaling
        vomma_min = min([x for x in self.vomma if x is not None])
        vomma_max = max([x for x in self.vomma if x is not None])
        self.vomma = [((x - vomma_min) / (vomma_max - vomma_min)) * scaling_factor if x is not None else None for x in self.vomma]



        # Epsilon Calculation
        self.epsilon = [
            -t * u * norm.cdf(d1_val)
            if t > 0 and u is not None and d1_val is not None
            else None
            for t, u, d1_val in zip(t_years, self.underlying_price, d1)
        ]

        # Volga Calculation
        self.volga = [
            (v * d1_val * d2_val / iv) if v and d1_val and d2_val and iv > 0 else None
            for v, d1_val, d2_val, iv in zip(self.vega, d1, d2, self.iv)
        ]

        # Normalize Volga with scaling
        volga_min = min([x for x in self.volga if x is not None])
        volga_max = max([x for x in self.volga if x is not None])
        
        self.volga = [((x - volga_min) / (volga_max - volga_min)) * scaling_factor if x is not None else None for x in self.volga]



        self.vera = [
            (v * d2_val / iv) if v and d2_val and iv > 0 else None
            for v, d2_val, iv in zip(self.vega, d2, self.iv)
        ]

        # Normalize Vera
        vera_min = min([x for x in self.vera if x is not None])
        vera_max = max([x for x in self.vera if x is not None])
        self.vera = [(x - vera_min) / (vera_max - vera_min) if x is not None else None for x in self.vera]


        self.data_dict = { 
            'option_symbol': self.ticker,
            'name': self.name,
            'ticker': self.underlying_symbol,
            'strike': self.strike,
            'call_put': self.contract_type,
            'expiry': self.expiry,
            'moneyness': self.moneyness,
            'volume': self.volume,
            'oi': self.oi,
            'iv': self.iv,
            'iv_percentile': self.iv_percentile,
            'delta': self.delta,
            'delta_theta_ratio': self.delta_to_theta_ratio,
            'gamma': self.gamma,
            'gamma_risk': self.gamma_risk,
            'theta': self.theta,
            'theta_decay_rate': self.theta_decay_rate,
            'vega': self.vega,
            'vega_impact': self.vega_impact,
            'charm': self.charm,
            'vera': self.vera,
            'volga': self.volga,
            'epsilon': self.epsilon,
            'vomma': self.vomma,
            'ultima': self.ultima,
            'speed': self.speed,
            'zomma': self.zomma,
            'veta': self.veta,
            'color': self.color,
            'vanna': self.vanna,
            'vanna_delta': self.vanna_delta,
            'vanna_vega': self.vanna_vega,
            'open': self.open,
            'high': self.high,
            'low': self.low,
            'close': self.close,
            'previous_close': self.previous_close,
            'intrinsic_value': self.intrinsic_value,
            'extrinsic_value': self.extrinsic_value,
            'change': self.change,
            'early_change': self.early_trading_change,
            'late_change': self.late_trading_change,
            'change_percent': self.change_percent,
            'early_change_percent': self.early_trading_change_percent,
            'late_change_percent': self.late_trading_change_percent,
            'last_trade_size': self.last_trade_size,
            'last_trade_price': self.last_trade_price,
            'last_trade_conditions': self.conditions,
            'bid': self.bid,
            'bid_size': self.bid_size,
            'bid_exchange': self.bid_exchange,
            'mid': self.midpoint,
            'ask': self.ask,
            'ask_size': self.ask_size,
            'ask_exchange': self.ask_exchange,
            'spread': self.spread,
            'spread_pct': self.spread_pct,
            'underlying_price': self.underlying_price,
            'option_profit_potential': self.opp,
            'liquidity_ratio': self.ltr,
            'option_sensitivity': self.oss,
            'risk_reward_score': self.rrs,
        }
        for k, v in self.data_dict.items():
            print(f"{k} LENGTH: {len(v)}")
        self.df = pd.DataFrame(self.data_dict)


    # Helper function to convert None to float and handle errors
    def safe_float(self, value):
        try:
            return float(value) if value is not None else None
        except (ValueError, TypeError):
            return None
