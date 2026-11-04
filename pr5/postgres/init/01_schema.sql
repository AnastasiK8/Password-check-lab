CREATE TABLE water (
    ts       timestamptz NOT NULL,
    station  text        NOT NULL,
    p        real        NOT NULL CHECK (p BETWEEN 0 AND 10),
    p_ema    real        NOT NULL,
    dp       real        NOT NULL,
    q        real        NOT NULL CHECK (q BETWEEN 0 AND 500),
    alarm    smallint    NOT NULL CHECK (alarm IN (0, 1)),
    lag_ms   integer     NOT NULL,
    PRIMARY KEY (station, ts)
);
CREATE INDEX water_ts_idx ON water (ts);

CREATE TABLE station_status (
    ts      timestamptz NOT NULL DEFAULT now(),
    station text        NOT NULL,
    online  smallint    NOT NULL CHECK (online IN (0, 1))
);
CREATE INDEX station_status_ts_idx ON station_status (ts);