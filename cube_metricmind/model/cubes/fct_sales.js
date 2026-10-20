/* cube(`FctSales`, {
  sql: `SELECT * FROM fct_sales`,

  joins: {
    DimCustomer: {
      sql: `${CUBE}.customer_id = ${DimCustomer}.customer_id`,
      relationship: `belongsTo`
    },
    DimProduct: {
      sql: `${CUBE}.product_id = ${DimProduct}.product_id`,
      relationship: `belongsTo`
    },
    DimRegion: {
      sql: `${CUBE}.region_id = ${DimRegion}.region_id`,
      relationship: `belongsTo`
    }
  },

  measures: {
    count: {
      type: `count`,
      title: `Total Orders`
    },

    totalRevenue: {
      sql: `order_amount`,
      type: `sum`,
      format: `currency`
    },

    totalProfit: {
      sql: `profit_amount`,
      type: `sum`,
      format: `currency`
    },

    avgProfitMargin: {
      sql: `profit_margin_percent`,
      type: `avg`
    },

    returnCount: {
      type: `count`,
      filters: [{ sql: `${CUBE}.returned = true` }]
    },

    returnRate: {
      sql: `CASE WHEN ${count} > 0 THEN 1.0 * ${returnCount} / ${count} ELSE 0 END`,
      type: `number`,
      format: `percent`
    }
  },

  dimensions: {
    orderId: {
      sql: `order_id`,
      type: `string`,
      primaryKey: true
    },

    customerId: {
      sql: `customer_id`,
      type: `string`
    },

    paymentMethod: {
      sql: `payment_method`,
      type: `string`
    },

    orderStatus: {
      sql: `order_status`,
      type: `string`
    },

    returned: {
      sql: `returned`,
      type: `boolean`
    },

    dateId: {
      sql: `date_id`,
      type: `time`
    }
  },

  preAggregations: {
    // Caches key sales metrics pre-grouped by region, customer segment, and day
    mainSalesRollup: {
      measures: [
        FctSales.count,
        FctSales.totalRevenue,
        FctSales.totalProfit,
        FctSales.returnCount
      ],
      dimensions: [
        DimCustomer.customerSegment,
        DimRegion.city,
        FctSales.paymentMethod,
        FctSales.orderStatus
      ],
      timeDimension: FctSales.dateId,
      granularity: `day`
    }
  }
}); */


cube(`FctSales`, {
  sql: `SELECT * FROM analytics.fct_sales`,

  joins: {
    DimCustomer: {
      sql: `${CUBE}.customer_id = ${DimCustomer}.customerId`,
      relationship: `belongsTo`
    },
    DimProduct: {
      sql: `${CUBE}.product_id = ${DimProduct}.productId`,
      relationship: `belongsTo`
    },
    DimRegion: {
      sql: `${CUBE}.region_id = ${DimRegion}.regionId`,
      relationship: `belongsTo`
    }
  },

  dimensions: {
    orderId: {
      sql: `order_id`,
      type: `string`,
      primaryKey: true
    },
    customerId: {
      sql: `customer_id`,
      type: `string`
    },
    productId: {
      sql: `product_id`,
      type: `string`
    },
    regionId: {
      sql: `region_id`,
      type: `number`
    },
    paymentMethod: {
      sql: `payment_method`,
      type: `string`
    },
    orderStatus: {
      sql: `order_status`,
      type: `string`
    },
    returned: {
      sql: `returned`,
      type: `boolean`
    },
    dateId: {
      sql: `date_id`,
      type: `time`
    }
  },

  measures: {
    count: {
      type: `count`,
      title: `Total Orders`
    },
    totalRevenue: {
      sql: `order_amount`,
      type: `sum`,
      format: `currency`
    },
    totalProfit: {
      sql: `profit_amount`,
      type: `sum`,
      format: `currency`
    },
    avgProfitMargin: {
      sql: `profit_margin_percent`,
      type: `avg`
    },
    returnCount: {
      sql: `CASE WHEN returned = true THEN order_id END`,
      type: `count`
    },
    returnRate: {
      sql: `1.0 * ${returnCount} / NULLIF(${count}, 0)`,
      type: `number`,
      format: `percent`
    }
  }
});