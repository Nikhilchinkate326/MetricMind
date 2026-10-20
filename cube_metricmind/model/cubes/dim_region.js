cube(`DimRegion`, {
  sql: `SELECT * FROM analytics.dim_region`,

  dimensions: {
    regionId: {
      sql: `region_id`,
      type: `number`,
      primaryKey: true
    },

    country: {
      sql: `country`,
      type: `string`
    },

    city: {
      sql: `city`,
      type: `string`
    },

    warehouseRegion: {
      sql: `warehouse_region`,
      type: `string`
    }
  }
});