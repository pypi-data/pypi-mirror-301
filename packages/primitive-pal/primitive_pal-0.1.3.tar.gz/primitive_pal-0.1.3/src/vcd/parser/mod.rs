#![allow(dead_code)] // Preserve other VCD parser features we might use later
/// Adapted from Rust VCD project (https://github.com/kevinmehall/rust-vcd)
use std::{
    borrow::Borrow,
    fmt::{self, Display},
};

use serde::{Deserialize, Serialize};

mod idcode;
pub use crate::vcd::parser::idcode::{IdCode, InvalidIdCode};

mod parser;
pub use crate::vcd::parser::parser::Parser;

mod scope;
pub use crate::vcd::parser::scope::{
    InvalidReferenceIndex, InvalidScopeType, InvalidVarType, ReferenceIndex, Scope, ScopeItem,
    ScopeType, Var, VarType,
};

mod timescale;
pub use crate::vcd::parser::timescale::{InvalidTimescaleUnit, TimescaleUnit};

mod value;
pub use crate::vcd::parser::value::{InvalidValue, Value, Vector};

mod write;

macro_rules! unit_error_struct {
    ($name:ident, $err:literal) => {
        #[doc = concat!("Parse error for ", $err, ".")]
        #[derive(Debug, Copy, Clone, PartialEq, Eq, Hash)]
        #[non_exhaustive]
        pub struct $name;

        impl Display for $name {
            fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
                write!(f, $err)
            }
        }

        impl std::error::Error for $name {}
    };
}
pub(crate) use unit_error_struct;

/// An element in a VCD file.
#[derive(Debug, PartialEq, Clone)]
#[non_exhaustive]
pub enum Command {
    /// A `$comment` command
    Comment(String),

    /// A `$date` command
    Date(String),

    /// A `$version` command
    Version(String),

    /// A `$timescale` command
    Timescale(u32, TimescaleUnit),

    /// A `$scope` command
    ScopeDef(ScopeType, String),

    /// An `$upscope` command
    Upscope,

    /// A `$var` command
    VarDef(VarType, u32, IdCode, String, Option<ReferenceIndex>),

    /// An `$enddefinitions` command
    Enddefinitions,

    /// A `#xxx` timestamp
    Timestamp(u64),

    /// A `0a` change to a scalar variable
    ChangeScalar(IdCode, Value),

    /// A `b0000 a` change to a vector variable
    ChangeVector(IdCode, Vector),

    /// A `r1.234 a` change to a real variable
    ChangeReal(IdCode, f64),

    /// A `sSTART a` change to a string variable
    ChangeString(IdCode, String),

    /// A beginning of a simulation command. Unlike header commands, which are parsed atomically,
    /// simulation commands emit a Begin, followed by the data changes within them, followed by
    /// End.
    Begin(SimulationCommand),

    /// An end of a simulation command.
    End(SimulationCommand),
}

/// A simulation command type, used in `Command::Begin` and `Command::End`.
#[derive(Debug, Copy, Clone, Eq, PartialEq)]
#[non_exhaustive]
#[allow(missing_docs)]
pub enum SimulationCommand {
    Dumpall,
    Dumpoff,
    Dumpon,
    Dumpvars,
}

impl Display for SimulationCommand {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        use SimulationCommand::*;
        write!(
            f,
            "{}",
            match *self {
                Dumpall => "dumpall",
                Dumpoff => "dumpoff",
                Dumpon => "dumpon",
                Dumpvars => "dumpvars",
            }
        )
    }
}

/// Structure containing the data from the header of a VCD file.
///
/// A `Header` can be parsed from VCD with [`Parser::parse_header`], or create an
/// empty `Header` with [`Header::default`].
#[derive(Debug, Default, Serialize, Deserialize)]
#[non_exhaustive]
pub struct Header {
    /// `$date` text
    pub date: Option<String>,

    /// `$version` text
    pub version: Option<String>,

    /// Parsed `$timescale` indicating the time unit used in the file
    pub timescale: Option<(u32, TimescaleUnit)>,

    /// Top-level variables, scopes, and comments
    pub items: Vec<ScopeItem>,
}

fn find_parent_scope<'a>(
    mut items: &'a [ScopeItem],
    path: &[impl Borrow<str>],
) -> Option<&'a [ScopeItem]> {
    for name in path {
        items = items.iter().find_map(|item| match item {
            ScopeItem::Scope(scope) if scope.identifier == name.borrow() => Some(&scope.items[..]),
            _ => None,
        })?;
    }
    Some(items)
}

impl Header {
    /// Find the scope object at a specified path.
    ///
    /// ## Example
    ///
    /// ```rust
    /// let mut parser = vcd::Parser::new(&b"
    /// $scope module a $end
    /// $scope module b $end
    /// $var integer 16 n0 counter $end
    /// $upscope $end
    /// $upscope $end
    /// $enddefinitions $end
    /// "[..]);
    /// let header = parser.parse_header().unwrap();
    /// let scope = header.find_scope(&["a", "b"]).unwrap();
    /// assert_eq!(scope.identifier, "b");
    /// ```
    pub fn find_scope<S>(&self, path: &[S]) -> Option<&Scope>
    where
        S: std::borrow::Borrow<str>,
    {
        let (name, parent_path) = path.split_last()?;
        let parent = find_parent_scope(&self.items, parent_path)?;

        parent.iter().find_map(|item| match item {
            ScopeItem::Scope(scope) if scope.identifier == name.borrow() => Some(scope),
            _ => None,
        })
    }

    /// Find the variable object at a specified path.
    ///
    /// ## Example
    ///
    /// ```rust
    /// let mut parser = vcd::Parser::new(&b"
    /// $scope module a $end
    /// $scope module b $end
    /// $var integer 16 n0 counter $end
    /// $upscope $end
    /// $upscope $end
    /// $enddefinitions $end
    /// "[..]);
    /// let header = parser.parse_header().unwrap();
    /// let var = header.find_var(&["a", "b", "counter"]).unwrap();
    /// assert_eq!(var.reference, "counter");
    /// ```
    pub fn find_var<S>(&self, path: &[S]) -> Option<&Var>
    where
        S: std::borrow::Borrow<str>,
    {
        let (name, parent_path) = path.split_last()?;
        let parent = find_parent_scope(&self.items, parent_path)?;

        parent.iter().find_map(|item| match item {
            ScopeItem::Var(v) if v.reference == name.borrow() => Some(v),
            _ => None,
        })
    }
}
