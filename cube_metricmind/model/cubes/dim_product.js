cube(`DimProduct`, {
  sql: `SELECT * FROM analytics.dim_product`,

  measures: {
    totalProducts: {
      type: `count`
    }
  },

  dimensions: {
    productId: {
      sql: `product_id`,
      type: `string`,
      primaryKey: true
    },

    category: {
      sql: `product_category`,
      type: `string`
    },

    subcategory: {
      sql: `product_subcategory`,
      type: `string`
    },

    brand: {
      sql: `brand`,
      type: `string`
    }
  }
});